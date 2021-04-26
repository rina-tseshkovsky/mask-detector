<html>
    % include('head.tpl')
    <body>
        % include('header.tpl')
		
        <h2>Restoreing File</h2>
        <form action="/rst-db" method="post">
            File Name: <input name="name" type="text" /><br>
            <input value="Restore This File" type="submit" />
            <input type="submit" name="bt1" value="Back" />
        </form>  

	</body>    
</html>