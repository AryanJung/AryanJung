<html>
<head>
    <style>
        form{
            background-color: antiquewhite;
            width: 220px;
            padding:20px;
            box-shadow: 10px 20px 30px ;
        }
        a{
            text-decoration: none;
            color: red;
        }
       
    </style>
</head>
<body>
    <form action="" method="POST" enctype="multipart/form-data">
        <input type="text" name="Name" id="" placeholder="Name">
        <br>
        <input type="Email" name="Email" id="" placeholder="Email">
        <br>
        <input type="tel" name="Phone" id="" placeholder="Phone">
        <br>
        Password 
        <br>
        <input type="password" name="Password" id="Password" placeholder="*Must contain 6 alphabets" size="30">
        <p id="Passerr"></p>
        <br>
        Confirm password
        <br>
        <input type="password" name="Cpassword" id="CPassword" placeholder="Confirm Password" size="30">
        <p id="Cpasserr"></p>
        <br>
        <input type="submit" name="Submit" id="">
    </form>

    <?php
    include 'dbconnect.php';
    if(isset($_POST['Submit']))
    {
        $Name=$_POST['Name'];
        $Email=$_POST['Email'];
        $Phone=$_POST['Phone'];
        $Password=$_POST['Password'];
        $Cpassword=$_POST['Cpassword'];
        $sql="Insert into signup 
        (Name,Email,Phone,Password,Cpassword)
        values('$Name','$Email','$Phone','$Password','$Cpassword')";
        $result=mysqli_query($conn,$sql);
        if($result)
        {
            echo "records were inserted succesfully";
        }
        else{
            echo "records were not inserted";
        }
    }
?>
</body>

</html>