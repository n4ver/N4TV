function copy_function() {
    /* Get the text field */
    var copyText = document.getElementById("sharelink");
  
    /* Select the text field */
    copyText.select();
    copyText.setSelectionRange(0, 99999); /* For mobile devices */
  
     /* Copy the text inside the text field */
    navigator.clipboard.writeText(copyText.value);
  
    /* Alert the copied text */
    var tooltip = document.getElementById("myTooltip");
    tooltip.innerHTML = "Copied!";
  }

  function out_function() {
    var tooltip = document.getElementById("myTooltip");
    tooltip.innerHTML = "Copy to clipboard";
  }