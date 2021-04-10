<html>
    % include('head.tpl')
    <body>
        % include('header.tpl')
        % include('toolbar.tpl')

        <form action="/add-user" method="post">
            User ID: {{usr_id}}<br>
            User Name: <input name="username" type="text" /><br>
            Password: <input name="password" type="text" /><br>
            <input value="Add New User" type="submit" />
        </form>  
    </body>    
</html>