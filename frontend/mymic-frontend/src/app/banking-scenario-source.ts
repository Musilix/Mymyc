import { BankingScenario } from '../app/banking-scenario';
import { ScenarioField } from '../app/scenario-field';
import { ScenarioSource } from '../app/scenario-source';

export class BankingScenarioSource extends ScenarioSource{
    constructor(data, cols){
        super(data, cols);
    }

    // setActiveRows(index, activatedScenario){
    //     this.activatedTableRows.set(index, activatedScenario);
    // }

    // getActiveRows(){
    //     return this.activatedTableRows;
    // }

    // getDormantRows(){
    //     return this.dormantTableRows;
    // }

    // getDataSource(){
    //     return this.BANKING_SCENARIO_DATA;
    // }

    // getDefinedCols(){
    //     return this.bankingDefinedCols;
    // }
}
