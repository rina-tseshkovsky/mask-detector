<html>
    % include('head.tpl')
    <body>
        % include('header.tpl')
        % include('toolbar.tpl')
        <form action="/users" method="post">
            <input type="submit" name="bt1" value="Add User" />
            <input type="submit" name="bt2" value="Delete User" />
            <input type="submit" name="bt3" value="Show All Users" />
            <input type="submit" name="bt4" value="Back" />
        </form> 
    </body>    
</html>