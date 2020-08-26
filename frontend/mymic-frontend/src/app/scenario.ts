import {ScenarioField} from './scenario-field';
export class Scenario {
    private Scenario: ScenarioField = new ScenarioField({fieldValue: "No Scenario Available"});
    private Gender: ScenarioField = new ScenarioField({fieldValue: false});
    private Address: ScenarioField = new ScenarioField({fieldValue: false});
    private DOB: ScenarioField = new ScenarioField({fieldValue: false});
    private firstName: ScenarioField = new ScenarioField({fieldValue: false});
    private lastName: ScenarioField = new ScenarioField({fieldValue: false});
    private Spouse_First_Name : ScenarioField = new ScenarioField({fieldValue: false});
    private Spouse_Last_Name : ScenarioField = new ScenarioField({fieldValue: false});
    private Spouse_DOB : ScenarioField = new ScenarioField({fieldValue: false});
    private Street_Address : ScenarioField = new ScenarioField({fieldValue: false});
    private Apt : ScenarioField = new ScenarioField({fieldValue: false});
    private City : ScenarioField = new ScenarioField({fieldValue: false});
    private County : ScenarioField = new ScenarioField({fieldValue: false});
    private Zip : ScenarioField = new ScenarioField({fieldValue: false});
    private State : ScenarioField = new ScenarioField({fieldValue: false});
    private Rent_or_Own : ScenarioField = new ScenarioField({fieldValue: false});
    private Email_Address : ScenarioField = new ScenarioField({fieldValue: false});
    private Primary_Phone : ScenarioField = new ScenarioField({fieldValue: false});
    private Secondary_Phone : ScenarioField = new ScenarioField({fieldValue: false});
    private Date_of_Purchase : ScenarioField = new ScenarioField({fieldValue: false});
    private Make : ScenarioField = new ScenarioField({fieldValue: false});
    private Model : ScenarioField = new ScenarioField({fieldValue: false});
    private Finance : ScenarioField = new ScenarioField({fieldValue: false});

    public constructor(init?:Partial<Scenario>) {
        Object.assign(this, init);
    }
}
