<html>
    % include('head.tpl')
    <body>
        % include('header.tpl')
		<h2>Purgeing Table</h2>
        <form action="/prg-tbl" method="post">
            Table Name: <input name="tbl_name" type="text" /><br>
            <input value="Purge" type="submit" />
            <input type="submit" name="bt1" value="Back" />
        </form>  
	</body>    
</html>