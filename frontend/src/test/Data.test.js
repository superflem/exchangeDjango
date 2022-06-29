import {controllaData} from '../js/ListTransactions';

describe("controlla data", () => {
    test("data corretta", () => {
        const data="2022-06-13";
        expect(controllaData(data)).toBe(true); //input corretto
    });
    test("data vuota", () => {
        const data="";
        expect(controllaData(data)).toBe(true); //input corretto
    });
    test("data con dimensione sbagliata", () => {
        const data="2022-06-3";
        expect(controllaData(data)).toBe(false); //input sbagliato (troppo corta)
    });
    test("controllo anno", () => {
        const data="d202-06-03";
        expect(controllaData(data)).toBe(false); //input sbagliato (anno)
    });
    test("controllo mese", () => {
        const data="2022-t6-03";
        expect(controllaData(data)).toBe(false); //input sbagliato (mese)
    });
    test("controllo giorno", () => {
        const data="2022-06-f3";
        expect(controllaData(data)).toBe(false); //input sbagliato (giorno)
    });
});