// A small model that exercises the lexical structure of KerML.
standard library package Vehicles {
    private import Base::*;
    private import ScalarValues::{Real, Boolean};

    doc /* Classifiers, features and expressions in KerML. */

    abstract classifier Vehicle specializes Anything;
    datatype Speed :> Real;
    struct Car :> Vehicle {
        feature wheels : Wheel[4] ordered nonunique;
        composite feature engine : Engine[1];
        derived var feature speed : Speed;
        const feature serial typed by Boolean;
        member feature spare : Wheel featured by Car;
    }
    class Wheel;
    class Engine;
    assoc Ownership {
        end feature owner : Car crosses owned.owner;
        end feature owned : Wheel;
    }
    disjoining Car disjoint from Wheel;
    specialization s subtype Car specializes Vehicle;
    behavior Drive { in feature distance : Real; }
    function Double { in x : Real; return : Real = x * 2; }
    predicate IsFast { in s : Speed; s > 1.5e2 }
    interaction Handshake;
    metaclass Tag;
    #Tag feature tagged : Car = new Car();
    feature v : Vehicle unions Car, Wheel;
    inv { true and not false }
    step drive : Drive;
    succession first drive then drive;
    connector c : Ownership from Car to Wheel;
    binding Car.engine = Car.engine;
    feature chained chains Car.engine;
    feature f inverse of Car.wheels;
    multiplicity many [0..*];
    namespace N;
    portion feature p : Car;
    type T conjugates Car;
    conjugation cj conjugate T conjugates Car;
    subclassifier Truck subset Car;
    redefinition rd redefinition Car::engine redefines Car::engine;
    typing tp typed Car typed by Vehicle;
    featuring ft of Car::engine by Car;
    differences Car, Wheel;
    intersects Car, Wheel;
    expr e { if true ? 1 else 2 }
    bool b { 1 == 1 }
    feature x = 1 + 2 * 3 - 4 / 5 % 6 ** 7 ^ 8;
    feature y = (null ?? 0) as Real;
    feature z = inverting.x;
    feature meta1 = Car meta KerML::Classifier;
    filter @KerML::Classifier;
    locale "en_US" /* A localized comment. */
    rep language "alf" /* this.x = 1; */
}
