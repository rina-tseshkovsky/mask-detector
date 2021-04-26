<html>
    % include('head.tpl')
    <body>
        % include('header.tpl')
		<h2>Purgeing Table</h2>
        <form action="/prg-db" method="post">
            File Name: <input name="name" type="text" /><br>
            <input value="Purge This File" type="submit" />
            <input type="submit" name="bt1" value="Back" />
        </form>  
	</body>    
</html>