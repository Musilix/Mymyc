export class Scenario {
    private Scenario: string = "No Scenario Available";
    private Gender: boolean = false;
    private Address: boolean = false;
    private DOB: boolean = false;
    private firstName: boolean = false;
    private lastName: boolean = false;
    private Spouse_First_Name : boolean = false;
    private Spouse_Last_Name : boolean = false;
    private Spouse_DOB : boolean = false;
    private Street_Address : boolean = false;
    private Apt : boolean = false;
    private City : boolean = false;
    private County : boolean = false;
    private Zip : boolean = false;
    private State : boolean = false;
    private Rent_or_Own : boolean = false;
    private Email_Address : boolean = false;
    private Primary_Phone : boolean = false;
    private Secondary_Phone : boolean = false;
    private Date_of_Purchase : boolean = false;
    private Make : boolean = false;
    private Model : boolean = false;
    private Finance : boolean = false;

    public constructor(init?:Partial<Scenario>) {
        Object.assign(this, init);
    }
}
