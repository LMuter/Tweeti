


$(document).ready(function() {
  window.previousTweets = [];
  window.nextTweets = [];
  init_window();
  $(".mdl-menu__item").click(function(e) {
    if ($(this).attr("disabled")) {
      console.log("disabled");
    } else {
      //$(this).attr("disabled", true);
      addLabel($(this).text());
    }
  });

  $(".logout-button").click(function(event) {
    window.location = "accounts/logout";
  });

  $(".login-button").click(function(event) {
    window.location = "accounts/login/";
  });

  $(".update-password").click(function(event) {
    window.location = "accounts/password_change/";
  });

  $("#prev_tweet_button").click(function(event) {
    previousTweet();
  });

  $("#next_tweet_button").click(function(event) {
    init_window();
  });

  $("#no-labels").click(function(event) {
    checkNoLabel();
  });

  $(".label-button").on("click", function(e) {
    handleLabelButton($(this));
  });

  $("#exclude_tweet_button").on("click", function(e) {
    if (confirm("Are you sure you want to exclude this tweet from the dataset?")) {
      console.log("exclude tweet");
      $.when(excludeTweet()).then(init_window());
    }
  });

  $("#discuss_tweet_button").on("click", function(e) {
    console.log("discuss tweet");
    $.when(discussTweet()).then(init_window());
  });

  $(".mdl-layout__header").on("click", function(event) {
    $("#average-displaytime").text(getAverageDisplayTime());
    $("#curr-displaytime").text(getCurrentDisplayTime());
    $("#num-tweets-displayed").text(getNumberOfTweetsDisplayed());
  });

  $(document).keyup(function( event ) {
    console.log(event.which);
    if ( event.which == 13 ) { // next tweet [return]
      init_window();
      console.log("next tweet PRESS");
    } else if (event.which == 8) { // previous tweet [backSpace]
      previousTweet();
      console.log("prev tweet PRESS");
    }
    event.preventDefault();
  });

  // Remove selected menu when user clicks outside menu
  $(document).click(function(event) {
    if (!$(event.target).is("button")) {
      menuItemSelected = undefined;
    }
  });

  var menuItemSelected;
  $(document).keypress(function(event) {
    if (isNull(menuItemSelected)) {
      triggerMenuSelect(event.key.toUpperCase());
    } else {
      triggerMenuItemSelect(event.key.toUpperCase());
    }
  });

  function triggerMenuSelect(key) {
    var menuSelect = $("button span.shortcut:contains(" + key + ")").parent();
    console.log(menuSelect);
    if (menuSelect.length > 0) {
      menuSelect.trigger('click');
      if ($("ul[for=" + menuSelect.attr('id') + "]").length > 0) {
        menuItemSelected = menuSelect;
      }
    }
  }

  function triggerMenuItemSelect(key) {
    var menuItem = $("ul[for=" + menuItemSelected.attr('id') + "] span.shortcut:contains(" + key + ")").parent();
    if (menuItem.length > 0) {
      addLabel(menuItem.text());
      $("#tweet_text").trigger('click');
      menuItemSelected = undefined;
    }
  }
});


function checkNoLabel() {
  handleLabelButton($("#no-labels"));
}


function canAddLabel(relatedMenuLenght, buttonId) {
  if (buttonId == "no-labels") {
    return window.tweet.labels.length == 0;
  }
  return relatedMenuLenght == 0;
}


function handleLabelButton($labelButton) {
  var $id = $labelButton.attr('id');
  var relatedMenu = $("ul[for=" + $id + "]");
  if (canAddLabel(relatedMenu.length, $id)) {
    var labelColor = getColorClass($labelButton);
    console.log($labelButton.text().trim());
    addLabel($labelButton.text().trim(), labelColor);
  }
}


function addLabel(labelText, labelColor) {
  if (!window.tweet.labels.includes(labelText)) {
    labelColor = labelColor || getLabelColor(labelText);
    addLabelChip(labelText, labelColor);
    let textSelection = getSelectionText();
    window.tweet.labels.push(labelText);
    if (textSelection) {
      window.tweet.selections = isNull(window.tweet.selections) ? {} : window.tweet.selections;
      window.tweet.selections[labelText] = textSelection;
    }
    console.log(window.tweet.labels);
    updateServerLabels();
  }
}


function init_window(prevTweet) {
  if (notNull(window.tweet) & isNull(prevTweet)) {
    window.tweet.displayTime += new Date() - window.tweet.displayStart;
    window.tweet.displayCount += 1;

    // add no-label when no labels are provided by user
    checkNoLabel();

    window.previousTweets.push(tweet);

    console.log("Average displaytime: " + getAverageDisplayTime());
    console.log("Current displaytime: " + getCurrentDisplayTime());
    console.log("Num of display: " + getNumberOfTweetsDisplayed());
  }
  window.tweet = null;
  $("#tweet_labels").text("")
  $("#tweet_text").text("")
  addSpinner();
  if (notNull(prevTweet)) {
    displayTweet(prevTweet);
  } else if (window.nextTweets.length > 0) {
    var nextTweet = window.nextTweets.pop();
    displayTweet(nextTweet);
    // fetch new tweets when last tweet is displayed
    if (window.nextTweets.length == 0) {
      fetchTweet(addNextTweet);
    }
  } else {
    fetchTweet(displayTweet);
  }
}


function addNextTweet(tweet) {
  console.log("additional Next Tweet");
  window.nextTweets.push(tweet)
}


function fetchTweet(callBack) {
  console.log("Fetch tweets");
  if (notNull(window.tweetRequest)) {
    window.tweetRequest.abort();
  }
  url = "tweet_data?n=10";
  window.tweetRequest = $.getJSON(url, function(data) {
    if (isNull(data.error)) {
      $.each( data.tweets, function( index, tweet ) {
        tweetLabelData = JSON.parse(tweet.labels);
        console.log(tweetLabelData);
        tweet.selections = tweetLabelData.selections;
        tweet.displayCount = tweetLabelData.displayCount;
        tweet.displayStart = tweetLabelData.displayStart;
        tweet.displayTime = tweetLabelData.displayTime;
        tweet.labels = tweetLabelData.labels;
        addNextTweet(tweet);
      });
      callBack(window.nextTweets.pop())
    } else {
      displayErrorMessage(data.error);
    }
  });
}


function previousTweet() {
  console.log(window.previousTweets);
  if (window.previousTweets.length > 0) {
    window.nextTweets.push(window.tweet);
    init_window(window.previousTweets.pop());
  } else {
    displayErrorMessage("No previous tweet");
  }
}


function displayTweet(tweet) {
  if (notNull(tweet)) {
    console.log(tweet);
    var labels = parseJson(tweet.labels);
    window.tweet = tweet;
    window.tweet.labels = parseLabels(labels);
    window.tweet.selections = parseSelections(tweet);
    window.tweet.displayTime = isNull(window.tweet.displayTime) ? 0 : window.tweet.displayTime;
    window.tweet.displayStart = new Date();
    window.tweet.displayCount = isNull(window.tweet.displayCount) ? 0 : window.tweet.displayCount;
    var fullText = isNull(tweet.tweet) ? "" : tweet.tweet.full_text;
    var tweetText = linkify(fullText);
    $("#tweet_text").html(tweetText);
    $("#tweet_url").html("<a href='" + tweet.tweet.url + "' target='_blank'>Source</a>");
    for(var n=0; n<window.tweet.labels.length;n++) {
      addLabelChip(tweet.labels[n], getLabelColor(tweet.labels[n]));
    }
  } else {
    init_window();
  }
}


function linkify(text) {
  var urlRegex =/(\b(https?|ftp|file):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/ig;
  return text.replace(urlRegex, function(url) {
    return '<a href="' + url + '">' + url + '</a>';
  });
}


function getAverageDisplayTime() {
  var sumDisplay = getCurrentDisplayTime();
  var numOfTweets = getNumberOfTweetsDisplayed();
  for(var n=0; n < numOfTweets - 1; n++) {
    sumDisplay += window.previousTweets[n].displayTime;
  }
  console.log("sumDisplay: " + sumDisplay);
  console.log("numOfTweets: " + numOfTweets);
  return Math.round(sumDisplay / numOfTweets);
}


function getCurrentDisplayTime() {
  if (notNull(window.tweet)) {
    var currDisplayTime = isNull(window.tweet.displayTime) ? 0 : window.tweet.displayTime;
    return currDisplayTime + (new Date() - window.tweet.displayStart);
  }
  return 0;
}


function notNull(o) {
  return !isNull(o);
}

function isNull(o) {
  return typeof o == 'undefined' || o == null
}


function getNumberOfTweetsDisplayed() {
  return window.previousTweets.length + 1;
}


function parseLabels(labels) {
  console.log(labels);
  if (isNull(labels)) {
    return [];
  } else {
    return labels;
  }
}


function parseSelections(tweet) {
  return tweet.selections || {};
}


function parseJson(s) {
  try {
    return JSON.parse(s);
  } catch(e) {
    return s;
  }
}


function addSpinner() {
  var spinner = $('<div class="mdl-spinner mdl-js-spinner is-active" id="main_spinner"></div>');
  $("#tweet_text").html(spinner);
}


function displayErrorMessage(errorMessage) {
  $("#tweet_text").text(errorMessage);
}


function updateServerLabels() {
  let url = "update_labels";
  let data = {
    "tweet_id": window.tweet.tweet.id,
    "labels": window.tweet.labels,
    "selections": window.tweet.selections,
    "displayTime": getCurrentDisplayTime(),
    "displayCount": window.tweet.displayCount + 1,
  };
  updateTweet(url, data);
}


function excludeTweet() {
  let url = "exclude_tweet";
  let data = {"tweet_id": window.tweet.tweet.id};
  updateTweet(url, data);
}


function discussTweet() {
  let url = "discuss_tweet";
  let data = {"tweet_id": window.tweet.tweet.id};
  updateTweet(url, data);
}


function updateTweet(url, data) {
  const csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value;

  const request = new Request(
    url,
    {headers: {
      'X-CSRFToken': csrf_token,
      'Content-Type': 'application/json',
    }}
  );
  fetch(request, {
    method: 'POST',
    mode: 'same-origin',  // Do not send CSRF token to another domain.
    body: JSON.stringify(data),
  }).then(function(response) {
    response.text().then(function(text) {
      console.log(text)
    });
  });
}




function addLabelChip(label_text, label_color) {
  var chipSpan = $('<span class="mdl-chip mdl-chip--deletable ' + label_color + '">');
  var chipText = $('<span class="mdl-chip__text">' + label_text + '</span>');
  var chipClose = $('<button type="button" class="mdl-chip__action close-chip"><i class="material-icons">cancel</i></button>');

  chipText.append(chipClose);
  chipSpan.append(chipText);

  $("#tweet_labels").append(chipSpan);

  chipClose.on("click", function() {
    const labelText = $(this).parent().parent().text().replace("cancel", "");

    console.log("close " + labelText);

    // todo handle if tweet is not found
    console.log(window.tweet);
    const index = window.tweet.labels.indexOf(labelText); // todo check unmatching text

    if (index > -1) {
      window.tweet.labels.splice(index, 1);
    }

    console.log(window.tweet.labels);

    $('#tweet_text').unmark();
    delete window.tweet.selections[labelText]
    console.log(window.tweet.selections);

    $(this).parent().parent().remove();
    updateServerLabels();
  });

  chipSpan.mouseenter(function() {
    console.log("hover chip.");
    let labelText = $(this).find('span').text().slice(0,-6);
    if (window.tweet.selections) {
      let selectionText = window.tweet.selections[labelText]; // todo check what happens when selections is empty
      console.log(selectionText);
      if (selectionText) {
        $('#tweet_text').mark(selectionText);
      }
    }
  }).mouseleave(function() {
    $('#tweet_text').unmark();
  });
}


function getLabelColor(labelText) {
  var menuItem = $("li:contains(" + labelText + ")");
  if (menuItem.length > 0) {
    return getColorClass(menuItem);
  }
  var buttonItem = $("button:contains(" + labelText + ")");
  if (buttonItem.length > 0) {
    return getColorClass(buttonItem);
  }
  console.log(buttonItem);
  return "gray_label";
}


function getColorClass($labelContainer) {
  var classList = $labelContainer.attr('class').split(/\s+/);
  for (var i = 0; i < classList.length; i++) {
    if (classList[i].startsWith("group-")) {
      return classList[i].substring(6);
    }
  }
  return "gray_label";
}


function getSelectionText() {
  var text = "";
  if (window.getSelection) {
    text = window.getSelection().toString();
  } else if (document.selection && document.selection.type != "Control") {
    text = document.selection.createRange().text;
  }
  return text;
}


window.post = function(url, data) {
  return fetch(url, {method: "POST", body: JSON.stringify(data)});
}


window.onerror = function errorNotifier(message, file, line, column, errorObj) {
  var errorData = {
    message: message, // e.g. ReferenceError
    file: file, // e.g. x is undefined
    url: document.location.href,
    line: line,
    column: column,
    stack: errorObj.stack, // stacktrace string; remember, different per-browser!
  };

  post("errornotifier", errorData);

  console.log(errorObj);
  return false;
}

