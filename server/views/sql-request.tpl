<html>
    % include('head.tpl')
    <body>
        % include('header.tpl')
        % include('toolbar.tpl')

        <form action="/sql-request" method="post">
            SQL Query: <input name="sql-query" type="text" /><br>
            <input value="Run SQL Query" type="submit" />
        </form>  
    </body>    
</html>