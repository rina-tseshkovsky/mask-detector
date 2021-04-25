<html>
    % include('head.tpl')
    <body>
        % include('header.tpl')

        <form action="/delete-user" method="post">
            Users Name: <input name="username" type="text" /><br>
            <input value="Delete this user" type="submit" />
            <input type="submit" name="bt1" value="Back" />
        </form>  

    </body>    
</html>