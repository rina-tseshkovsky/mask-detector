<html>
    % include('head.tpl')
    <body>
        % include('header.tpl')

        <form action="/delete-sensor" method="post">
            Sensors UUID: <input name="UUID" type="text" /><br>
            <input value="Delete this sensor" type="submit" />
        </form>  

    </body>    
</html>