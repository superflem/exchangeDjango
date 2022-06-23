import {controllaSoldi, controllaValuta} from '../js/Buy';

describe("login", () => {
    test("convalida i soldi", () => {
        const soldi = 12;
        const max = 12;
        expect(controllaSoldi(soldi, max)).toBe(true); //input corretto
    });
    test("convalida i soldi", () => {
        const soldi = 12;
        const max = -1;
        expect(controllaSoldi(soldi, max)).toBe(true); //input corretto (con massimo a -1)
    });
    test("convalida i soldi non validi", () => {
        const soldi = 13;
        const max = 12;
        expect(controllaSoldi(soldi, max)).toBe(false); //input errato (oltre il massimo)
    });

    test("convalida i soldi non validi", () => {
        const soldi = "eegr";
        const max = 12;
        expect(controllaSoldi(soldi, max)).toBe(false); //input errato (soldi come stringa)
    });
});

describe("password", () => {
    test("convalida la valuta", () => {
        const valuta = "EUR";
        expect(controllaValuta(valuta)).toBe(true); //input corretto
    });
    test("convalida la valuta", () => {
        const valuta = "USD";
        expect(controllaValuta(valuta)).toBe(true); //input corretto
    });
    test("convalida la valuta non valida", () => {
        const valuta = "prova"
        expect(controllaValuta(valuta)).toBe(false); //input errato
    });
});