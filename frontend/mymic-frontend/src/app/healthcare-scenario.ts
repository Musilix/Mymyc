import { ScenarioField } from '../app/scenario-field';

export class HealthcareScenario {
    private Scenario: ScenarioField = new ScenarioField({fieldValue: "No Scenario Available"});
    private Account : ScenarioField = new ScenarioField({fieldValue: false});
    private Account_Holder : ScenarioField = new ScenarioField({fieldValue: false});
    private Account_Identifier : ScenarioField = new ScenarioField({fieldValue: false});
    private Account_Number : ScenarioField = new ScenarioField({fieldValue: false});

    constructor(init ?: Partial<HealthcareScenario>){
        Object.assign(this, init);
    }
}
