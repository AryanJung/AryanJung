<html>
    <head>
        <style>
            a{
                text-decoration: none;
                color: red;
            }
            table{
                width: 100%;
                text-align: center;
            }
            button{
                width: 100px;
                background-color: black;
                height: 50px;
            }
        </style>
    </head>
    <body>
        <table border="1px" cellpadding="5">
            <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Phone</th>
                <th>Password</th>
                <th>Cpassword</th>
            </tr>
            <?php
include 'dbconnect.php';
$sql="select * from signup";
$result=mysqli_query($conn,$sql);
$num=mysqli_num_rows($result);
if($num>0)
{
    while($row=mysqli_fetch_assoc($result))
    {
   
        ?>
        <tr>
            <td> <?php echo $row['Name']?></td>
            <td> <?php echo $row['Email']?></td>
            <td> <?php echo $row['Phone']?></td>
            <td> <?php echo $row['Password']?></td>
            <td> <?php echo $row['Cpassword']?></td>
        </tr>
        <?php
         }
   
}
            ?>
        </table>
    </body>
</html>