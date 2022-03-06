<!-- db1.php
     A PHP script to access the movie database
     through MySQL

     Query #1: See the requested number of actors.
     -->
<html>
<head>
<title> Access the cars database with MySQL </title>
<link rel="stylesheet" type="text/css" href="style.css" />
</head>
<body>
<?php

// Connect to MySQL

// How does the user know which ID to use? The backend needs to assign the ID,
// not the front end. Front end is just something you need to get from the user.
// Think about this.

// Trigger? It's not going to work in 10 days.

$servername = "cs100.seattleu.edu";
$username = "user24";
$password = "1234abcdF!";

$conn = mysql_connect($servername, $username, $password);

if (!$conn) {
     print "Error - Could not connect to MySQL ".$conn;
     exit;
}

// change to your default db for PDA6!!!
$dbname = "bw_db24";

$db = mysql_select_db($dbname, $conn);
if (!$db) {
    print "Error - Could not select the movie database ".$dbname;
    exit;
}


// These names should match the corresponding names in HTML.

$num_actors = $_POST['displayActors']; // stores the value entered in the displayActors form


// testing purpose (remove it after you complete testing!!!)
print "Number of actors to display: ".$num_actors."<br />";


// Clean up the given query (delete leading and trailing whitespace)
trim($num_actors);

// remove the extra slashes

$num_actors = stripslashes($num_actors);


// Make the query using the values from the user input.
// Dot operator: String concatenation.
// Put a semicolon for the MySQL statement.

$query = 'select * from Actor;';


// Testing (remove it when testing is done!!!)
print "<p>Actor Query: ".$query."</p>";


// Execute the query
$result = mysql_query($query);

if (!$result) {
    print "Error - the query could not be executed";
    $error = mysql_error();
    print "<p>" . $error . "</p>";
    exit;
}

// Get the number of rows in the result
$num_rows = mysql_num_rows($result);

print "Number of rows = $num_rows <br />";

// Get the number of fields in the rows
$num_fields = mysql_num_fields($result);
print "Number of fields = $num_fields <br />";

// Get the first row
$row = mysql_fetch_array($result);

// Display the results in a table
print "<table border='border'><caption> <h2> Query Results </h2> </caption>";
print "<tr align = 'center'>";

// Produce the column labels
$keys = array_keys($row);
for ($index = 0; $index < $num_fields; $index++) 
    print "<th>" . $keys[2 * $index + 1] . "</th>";

print "</tr>";

// Output the values of the fields in the rows
for ($row_num = 0; $row_num < $num_rows; $row_num++) {

    print "<tr align = 'center'>";
    $values = array_values($row);
	
    for ($index = 0; $index < $num_fields; $index++){
        $value = htmlspecialchars($values[2 * $index + 1]);
        print "<td>" . $value . "</td> ";
    }

    print "</tr>";
    $row = mysql_fetch_array($result);
}

print "</table>";

mysql_close($conn);
?>

<br /><br />
<a href="http://css1.seattleu.edu/~dstanko/dbtest/PDA6_db.html"> Go to Main Page </a>

</body>
</html>
