namespace Soctec.Icppi.NN.Logic.Account

open Soctec.Icppi.NN.Model.Cppi
open Soctec.Icppi.NN.Model.Cppi.Errors
open Soctec.Icppi.NN.Model.Cppi.Measures
open Soctec.Icppi.NN.Logic.Account.Common

module AccountState =

    let notLocked (plan: PlanParameters) acs validIfClosing =
        match acs with
        | Running | Suspended -> true, ""
        | Closing -> if validIfClosing then true, "" else false, "Account is locked"
        | Defeasing when not plan.Switches.LockAccountWhileDefeasing -> true, ""
        | Defeased when not plan.Switches.LockAccountWhileDefeasing -> true, ""
        | _ -> false, "Account is locked"

    let initial va = 
        getPrevValue va (fun a -> a.State) Running

    let cancellation vstate astate ac (iac: option<AccountCancellationRequest>) ow = 
        elb {
            //We received a cancellation request or have one pending (and have not yet started the cancellation process)
            let ac = match ac, iac with
                     | Some(acr), _ -> Some(acr)
                     | _, Some(acr) -> Some(acr)
                     | _, _ -> None

            match astate, ac with
            | Defeased, Some(acr) -> if not ow && isAccountLiquidated vstate then return Closed else return Closing
            | Defeased, None -> return Defeased
            | Defeasing, Some(acr) -> if not ow && isAccountLiquidated vstate then return Closed else return Closing
            | Defeasing, _ when isAccountInProtection vstate -> return Defeased
            | Defeasing, _ -> return Defeasing
            | Closing, _ when isAccountLiquidated vstate -> return Closed
            | Closing, _ -> return Closing
            | Suspended, Some(acr) when isAccountLiquidated vstate -> return Closed
            | Suspended, Some(acr) -> return Closing
            | Suspended, None -> return Suspended
            | Running, Some(acr) when not ow && isAccountLiquidated vstate -> return Closed
            | Running, Some(acr) -> if not ow then return Closing else return Running
            | Running, None -> return Running
            | _ -> return! error (AccountError(InvalidAccountState)) Error (sprintf "Unexpected account state %A (when determining cancellation state)" astate) astate
        }

    let suspend astate fw =
        elb {
            match astate, fw with
            | Defeased, _ -> return Defeased
            | Defeasing, _ -> return Defeasing
            | Closing, _ -> return Closing
            | Closed, _ -> return Closed
            | Running, Some(fwth) -> return Suspended
            | Running, None -> return Running
            | Suspended, _ -> return Suspended
            //| _ -> return! error (AccountError(InvalidAccountState)) Error (sprintf "Unexpected account state %A (when determining suspended state)" astate) astate
        }

    let defeasance acs (c: amount) (cptg: decimal) (hwmw: amount) (plan:PlanParameters) =
        let trigger = if plan.Switches.CushionNIVPtgTriggersDefeasance then
                         cptg
                      else    
                        if hwmw = 0.0m<amount'> then 1.0m else c / hwmw
        
        match acs with
        | Running when trigger < plan.Economics.MinimumCushion -> Defeasing
        | _ -> acs

    let reinvest (plan: PlanParameters) acs efv cptg =
        let canReinvest = plan.Switches.RebalanceOnMinimumCushion && efv = 0m<amount'> && cptg > plan.Economics.ReleverageCushion
        
        match acs with
        | Defeasing when canReinvest -> Running
        | Defeased when canReinvest -> Running
        | _ -> acs

    let restart acs (da: amount) =
        match acs with
        | Suspended when da > 0m<amount'> -> Running
        | _ -> acs
