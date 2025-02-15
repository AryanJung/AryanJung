<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <style>
    #A{
        font-size: 25px;
        font-family:cursive;
    }
    body{
            background-image: url(backgroundlogin.jpg);
            background-repeat: no-repeat;
            background-size: 100% ;   
        }
        #B{
            /* float: center; */
           background-color: aliceblue;
            position: absolute;
            width: 400px;
            height: 600px;
            right: 38%;
            opacity: 0.8;
            top: 10%;
            border-radius: 40px;
        }
        input{
            
        border-style:hidden;
        border-bottom-style: inset;
        /* border-radius: 20px; */
        padding: 10px 15px;
        border-radius: 10px;
        }
        .SUBMIT{
        
        width: 40%;
        border: none;
        border-radius: 30px;
        background: linear-gradient(to left, rgba(95,255,255,1) 0%, rgba(113,79,235,1) 100%);;
        padding: 10px 25px;
        font-size: 16px;
        cursor: pointer;
        text-align: center;
     }
    .HOME{
    font-size: 40px;
}
.a{
    text-decoration:none;
}
    </style>
</head>
<body>
    <a href="Html.html" class="HOME"><ion-icon name="home-outline"></ion-icon></a>
       
    <form align="center" id="B" method="POST" enctype="multipart/form-data">
        <legend id="A" ><b>Register</b></legend>
        <br>
        Name 
        <br>
        <input type="text" name="Name" id="Name" placeholder="Name" autocomplete="none" size="30">
        <p id="Nameerr"></p>
        <br>
        Email 
        <br>
        <input type="email" name="Email" id="Email" placeholder="Email" autocomplete="none" size="30">
        <p id="Emailerr"></p>
        <br>
        Phone number
        <br>
        <input type="tel" name="Phone" id="Phone" placeholder="Phone No(10 digits)" size="30">
        <p id="Phoneerr"></p>
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
        <input type="submit" name="Submit" class="SUBMIT">
        <button class="SUBMIT"><a href="view.php" class="a">View Database</a></button>
    </form>
    <script>
        function validate()
        {
            let name=document.getElementById('Name').value;
            let namereg=/[a-z A-Z]/;
            if(name===''||name==null)
            {
                document.getElementById('Nameerr').innerHTML="Required!";
                return false;
            }
            
       
        else if(name.search(namereg)<0)
        {
            document.getElementById('Nameerr').innerHTML="name pattern is not matched";
            return false;
        }
        let email=document.getElementById('Email').value;
            let emailreg=/[a-z A-Z 0-9]\@gmail\.com/;
            if(email===''||email==null)
            {
                document.getElementById('Emailerr').innerHTML="Required!";
                return false;
            }
            
       
        else if(email.search(emailreg)<0)
        {
            document.getElementById('Emailerr').innerHTML="Email pattern is not matched";
            return false;
        }
        let phone=document.getElementById('Phone').value;
      let phonereg=/[0-9]{10}/;
      if(phone===''||phone==null)
      {
            document.getElementById('Phoneerr').innerHTML='Required!';
            return false;
      }
      else if(phone.search(phonereg)<0)
      {
            document.getElementById('Phoneerr').innerHTML='*Phone pattern is not matched';
            return false;
      }
      else 
      {
        document.getElementById('Phoneerr').innerHTML='';
        
      }
      
      
      let pass=document.getElementById('Password').value;
      let passreg=/[a-z A-Z]{6}/;
      if(pass===''||pass==null)
      {
            document.getElementById('Passerr').innerHTML='*Password can not be empty';
            return false;
      }
      else if(pass.search(passreg)<0)
      {
            document.getElementById('Passerr').innerHTML='*Password must contain only alphabet upto 6 characters';
            return false;
      }


      let Cpass=document.getElementById('CPassword').value;
      let Cpassreg=/[a-z A-Z]{6}/;
      if(Cpass===''||Cpass==null)
      {
            document.getElementById('Cpasserr').innerHTML='Required!';
            return false;
      }
      else if(Cpass.search(Cpassreg)<0)
      {
            document.getElementById('Cpasserr').innerHTML='*Password pattern is not matched';
            return false;
      }
      else if(pass!=Cpass)
      {
        document.getElementById('Cpasserr').innerHTML='*Password is not same';
            return false;
      }
    }
    </script>
    <script type="module" src="https://unpkg.com/ionicons@7.1.0/dist/ionicons/ionicons.esm.js"></script>
    <script nomodule src="https://unpkg.com/ionicons@7.1.0/dist/ionicons/ionicons.js"></script>
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
