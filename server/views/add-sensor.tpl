<html>
    % include('head.tpl')
    <body>
        % include('header.tpl')
        % include('toolbar.tpl')

        <form action="/add-sensor" method="post">
            Sensor UUID: <input name="UUID" type="text" /><br>
            Password: <input name="password" type="text" /><br>
            <input value="Add New Sensor" type="submit" />
        </form>  
    </body>    
</html>