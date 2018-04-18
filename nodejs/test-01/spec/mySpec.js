describe("Random", function() {
    //var Player = require('../../lib/jasmine_examples/Player');
    //var Song = require('../../lib/jasmine_examples/Song');
    var player;
    var song;
  
    beforeEach(function() {
      inNumber = 0;
      outNumber = 0;
    });
  
    it("should generate numbers", function() {

      expect(inNumber).toEqual(outNumber+1);

    });
});
