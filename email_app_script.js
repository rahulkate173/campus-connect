function sendAbsenceEmails() {
  // PASTE YOUR ID BETWEEN THE QUOTES BELOW
  var ss = SpreadsheetApp.openById("1q4Eua92DZvpVP2AF8x2iLA51wyvA4ZCAeaGZ2EKHsUo");
  
  // This gets the very first tab regardless of its name
  var sheet = ss.getSheets()[0]; 
  
  var data = sheet.getDataRange().getValues();
  var count = 0;
  
  for (var i = 1; i < data.length; i++) {
    var studentName = data[i][1]; // Column A
    var status = data[i][2];      // Column B
    var parentEmail = data[i][3]; // Column C
    
    if (status && status.toString().trim().toLowerCase() === "absent") {
      if (parentEmail && parentEmail.includes("@")) {
        var subject = "Absence Notification: " + studentName;
        var message = "Dear Parent,\n\nThis is to inform you that " + studentName + 
                      " was marked absent in today's DBMS lecture.\n\nRegards AI&DS Dept PVG COETM,\nSchool Office";
        
        MailApp.sendEmail(parentEmail, subject, message);
        count++;
      }
    }
  }
  Logger.log("Execution complete. Emails sent: " + count);
}