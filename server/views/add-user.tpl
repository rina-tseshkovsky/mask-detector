<html>
    % include('head.tpl')
    <body>
        % include('header.tpl')

        <form action="/add-user" method="post">
            User ID: {{usr_id}}<br>
            User Name: <input name="username" type="text" /><br>
            Password: <input name="password" type="text" /><br>
            <input value="Add New User" type="submit" />
            <input type="submit" name="bt1" value="Back" />

        </form>  
    </body>    
</html>