// A small drone model that exercises the lexical structure of SysML v2.
package 'Drone Example' {
    private import ScalarValues::*;
    private import ISQ::*;
    public import SI::{kg, m, s};

    //* A multiline note.
        The parser ignores it, unlike the regular comments below. */

    doc /* Models of a small quadcopter, see https://www.omg.org/spec/SysML/. */

    comment Units about Drone
        /* All values are in SI units. */

    metadata def Safety {
        attribute isMandatory : Boolean default true;
    }
    metadata def <ss> SafetySpecific :> Metaobjects::SemanticMetadata {
        :>> baseType = drones meta SysML::PartUsage;
    }

    abstract part def Vehicle;

    part def Drone :> Vehicle {
        doc /* A drone with four rotors. */
        attribute mass : MassValue = 1.25 [kg];
        attribute 'max. speed' : SpeedValue = 2.0E1 [m/s];
        attribute serial : String = "DR-01 \"alpha\"";
        attribute manual : String = "https://example.org/drones"; // Don't "quote" notes.
        attribute flightTime : TimeValue[0..1];

        #Safety part battery : Battery {
            attribute capacity : Real = 5.4e3;
        }
        part rotors : Rotor[4] ordered nonunique;
        port controlPort : ~ControlPort;
        ref part pilot : Pilot[0..*];

        constraint { mass <= 2 [kg] and flightTime >= 900 [s] }
    }

    part def Battery;
    part def Rotor;
    part def Pilot;
    port def ControlPort { in attribute command : String; }

    part drones : Drone[*];
    #SafetySpecific part drone : Drone {
        @Safety { isMandatory = false; }
    }

    action def Fly {
        in item target;
        out attribute success : Boolean;
        first start then takeOff;
        action takeOff;
        then action cruise;
        then done;
    }

    state def FlightStates {
        entry; then idle;
        state idle;
        transition idle_to_flying
            first idle
            accept Command
            if drone.battery.capacity > .5
            do action launch
            then flying;
        state flying;
    }

    requirement def <'R1.1'> MaxMass {
        subject drone : Drone;
        require constraint { drone.mass <= 2 [kg] }
    }

    calc def Average {
        in values : Real[1..*];
        return result : Real = sum(values) / size(values);
    }

    attribute selected = drones->select { in d : Drone; d.mass < 1.5 [kg] };
    attribute first = selected#(1);
    attribute isDrone = drone @ Drone and drone istype Vehicle
        and not (drone hastype Rotor) xor false implies true;
    attribute isPart = drone @@ SysML::PartUsage;
    attribute name = drone.?{ in d; d.serial != null } ?? "none";
    attribute total = (1 + 2 * 3 - 4 / 5 % 6) ** 2 ^ 1;
    attribute same = drone === drone or drone !== drones;
    attribute rootName = $::'Drone Example'::Drone;

    rep inOCL language "ocl" /* self.mass <= 2 */
}
