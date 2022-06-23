import {controllaEmail, controllaPassword} from '../js/Login';

describe("login", () => {
    test("convalida la email", () => {
        const email = "test@test.it";
        expect(controllaEmail(email)).toBe(true); //input corretto
    });
    test("convalida la email non valida", () => {
        const email = "testsenzachiocciola.it";
        expect(controllaEmail(email)).toBe(false); //input errato
    });
});

describe("password", () => {
    test("convalida la password", () => {
        const password = "acd3a2ca97dd545afc16ccb52e497d42a0a05342215c15d5e4f56ccc69ab7e947bf98353b57a3cad8b2268714aae4ae7ac8653dee473a3d0a71c32e8da4d174b";
        expect(controllaPassword(password)).toBe(true); //input corretto
    });
    test("convalida la password non valida", () => {
        const password = "testsenzachiocciola.it";
        expect(controllaPassword(password)).toBe(false); //input errato
    });
});