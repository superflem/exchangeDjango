import {controllaIban} from '../js/Signup';

describe("iban", () => {
    test("convalida l'iban", () => {
        const iban = "IT4738495737201938475637281";
        expect(controllaIban(iban)).toBe(true); //input corretto
    });
    test("convalida l'iban non valido", () => {
        const iban = "IT36978";
        expect(controllaIban(iban)).toBe(false); //input errato
    });
});