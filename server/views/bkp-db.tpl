<html>
    % include('head.tpl')
    <body>
        % include('header.tpl')
		
        <h2>Backuping File</h2>
        <form action="/bkp-db" method="post">
            File Name: <input name="name" /><br>
            <input value="Backup This File" type="submit" />
            <input type="submit" name="bt1" value="Back" />
        </form>  

	</body>    
</html>