function ans(cell) {
    // Get the active spreadsheet
    var ss = SpreadsheetApp.getActive();
    
    // Get the main sheet named 'Sheet1'
    var mainSheet = ss.getSheetByName('Sheet1');
    
    // Get the data from the cell
    var data = cell;
    
    // Log the data
    Logger.log(data);
    
    // Set the URL for the endpoint, change it accordingly based on your specific setup
    var url = 'https://8b80-2401-4900-1c6e-d3b5-3d5b-ed27-4801-b9d1.ngrok-free.app/predict?question=' + data;
    
    // Set the options for the HTTP request
    var options = {
      'method': 'GET',
      'headers': {
        "ngrok-skip-browser-warning": false
      }
    };
    
    // Send the HTTP request to the endpoint
    var response = UrlFetchApp.fetch(url, options);
    
    // Return the content of the response
    return response.getContentText();
  }
  