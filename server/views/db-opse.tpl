<html>
    % include('head.tpl')
    <body>
        % include('header.tpl')
        Data Base Operations
		<form action="/dbops" method="post">
            <input type="submit" name="bt1" value="Backup DB" />
            <input type="submit" name="bt2" value="Restore DB" />
            <input type="submit" name="bt3" value="Purge Table" />
            <input type="submit" name="bt4" value="Back" />
        </form> 
    </body>    
</html>