export class ScenarioField {
    private fieldValue : any;
    private required : boolean = false;

    constructor(init ?: Partial<ScenarioField>){
        Object.assign(this, init);
    }
}
