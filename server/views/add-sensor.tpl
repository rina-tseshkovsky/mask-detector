<html>
    % include('head.tpl')
    <body>
        % include('header.tpl')

        <form action="/add-sensor" method="post">
            Sensor UUID: <input name="uuid" type="text" /><br>
            Password: <input name="password" type="text" /><br>
            <input value="Add New Sensor" type="submit" />
            <input type="submit" name="bt1" value="Back" />
        </form>  
    </body>    
</html>