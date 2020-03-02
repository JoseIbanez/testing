describe("sample", function() {
    var sample = System.getModule("com.vodafone.ci.test.test2").sample;
    it("should add two numbers", function() {
        expect(sample(5, 2)).toBe(7);
    });
});
