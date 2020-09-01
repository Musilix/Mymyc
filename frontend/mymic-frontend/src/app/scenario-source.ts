export class ScenarioSource {
    private dormantTableRows = new Map<number, any>();
    private activatedTableRows = new Map<number, any>();
    private data : any;
    private cols : string[];

    constructor(data, cols){
        let iterator = 0;
        this.cols = cols;
        this.data = data;
        this.data.forEach((scenario: any) => {
            this.dormantTableRows.set(iterator, scenario);
            iterator++;
        });
    }

    setActiveRows(index, activatedScenario){
        this.activatedTableRows.set(index, activatedScenario);
    }

    getActiveRows(){
        return this.activatedTableRows;
    }

    getDormantRows(){
        return this.dormantTableRows;
    }

    getDataSource(){
        return this.data;
    }

    getDefinedCols(){
        return this.cols;
    }
}
