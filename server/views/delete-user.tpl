<html>
    % include('head.tpl')
    <body>
        % include('header.tpl')
        % include('toolbar.tpl')

        <form action="/delete-user" method="post">
            User ID: {{usr_id}}<br>
            Users Name: <input name="username" type="text" /><br>
            <input value="Delete this user" type="submit" />
        </form>  

    </body>    
</html>