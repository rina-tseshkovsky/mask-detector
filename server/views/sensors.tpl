<html>
    % include('head.tpl')
    <body>
        % include('header.tpl')
        % include('toolbar.tpl')
        <form action="/sensors" method="post">
            <input type="submit" name="bt1" value="Add Sensor" />
            <input type="submit" name="bt2" value="Delete Sensor" />
            <input type="submit" name="bt3" value="Show All Sensors" />
            <input type="submit" name="bt4" value="Back" />
        </form> 
    </body>    
</html>