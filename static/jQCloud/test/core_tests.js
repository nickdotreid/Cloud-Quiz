var some_words = [
  {text: 'Zero', weight: 0},
  {text: 'Minus three', weight: -3},
  {text: 'Minus zero point fiftyfive', weight: -0.55},
  {text: 'Two', weight: '2.0', url: '#'}
];

var some_other_words = [
  {text: 'Abc', weight: 1},
  {text: 'Def', weight: 2},
  {text: 'Ghi', weight: 3}
];

$(document).ready(function() {
  $("#container").jQCloud(some_words, {callback: function() {
    
    test('Basic plugin functionality', function() {
      var text = $("#container").text();
      ok(text.search(/Zero/) >= 0, "'Zero' is in the cloud");
      ok(text.search(/Minus three/) >= 0, "'Minus three' is in the cloud");
      ok(text.search(/Minus zero point fiftyfive/) >= 0, "'Minus zero point five' is in the cloud");
      ok(text.search(/Two/) >= 0, "'Two' is in the cloud, even if the weight was a string");
      
      var biggest = $("#container_word_0");
      equals(some_words[0].text, "Two", "'Two', having the biggest weight, becomes the first element in the array");
      equals(biggest.text(), "Two", "'Two', having the biggest weight, gets wrapped in an element of id container_word_0");
      ok(biggest.hasClass("w10"), "the element with the biggest weight gets wrapped in an element of class w10");
      
      var smallest = $("#container_word_" + (some_words.length - 1));
      equals(some_words[(some_words.length - 1)].text, "Minus three", "'Minus three', having the smallest weight, becomes the last element in the array");
      equals(smallest.text(), "Minus three", "'Minus three', having the smallest weight, gets wrapped in an element of id container_word_"+(some_words.length - 1));
      ok(smallest.hasClass("w1"), "the element with the smallest weight gets wrapped in an element of class w1");
      
      var middle = $("#container_word_2");
      equals(middle.text(), "Minus zero point fiftyfive", "'Minus zero point fiftyfive' should get wrapped in an element of id container_word_2");
      ok(middle.hasClass("w5") && middle.text() == "Minus zero point fiftyfive", "'Minus zero point fiftyfive', having a weight in the middle of the range, should get wrapped in an element of class w5");
      
    });
    
    test('links into word cloud', function() {
      ok($("#container span:contains('Two') a[href=#]").length == 1, "If 'url' parameter is specified, an html anchor pointing to that URL is created.");
    })
    
  }});
  
  $("#container2").jQCloud(some_other_words, {width: 200, height: 100, delayed_mode: true, randomClasses: 2, callback: function() {
    
    test('Multiple word clouds rendering, also with delayed_mode: true', function() {
      var text = $("#container2").text();
      ok(text.search(/Abc/) >= 0, "'Abc' is in the second cloud");
      ok(text.search(/Def/) >= 0, "'Def' is in the second cloud");
      ok(text.search(/Ghi/) >= 0, "'Ghi' is in the second cloud");
      ok(text.search(/Zero/) < 0, "'Zero' is not in the second cloud");
    });
    
    test("Option randomClasses", function() {
      ok($("#container2 span.w1").hasClass("r1") || $("#container2 span.w1").hasClass("r2"), "Since randomClasses = 2, each word should be assigned randomly either to class 'r1' or 'r2'");
    });
    
    $("#container2").html(""); // Clean container2
    
    $("#container2").jQCloud(some_other_words, {width: 200, height: 100, delayed_mode: true, randomClasses: [true, false], callback: function() {
      
      test("Option randomClasses with array", function() {
        ok($("#container2 span.w1").hasClass("true") || $("#container2 span.w1").hasClass("false"), "Since randomClasses = [true, false], each word should be assigned randomly either to class 'true' or 'false'");
      });
      
    }});
    
  }});
});
