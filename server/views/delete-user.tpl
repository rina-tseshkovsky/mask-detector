<html>
    % include('head.tpl')
    <body>
        % include('header.tpl')
        % include('toolbar.tpl')

        <form action="/delete-user" method="post">
            Users Name: <input name="username" type="text" /><br>
            <input value="Delete this user" type="submit" />
        </form>  

    </body>    
</html>