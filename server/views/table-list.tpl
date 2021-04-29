<html>
    % include('head.tpl')
    <body>
        % include('header.tpl')
		
        <h2>{{lst_header}}</h2>
        <form action="/file-list" method="post">
            <input type="submit" name="bt1" value="Back" />
        </form>
		<table style="width:100%">
			% for member in lst_data:
				<tr>
					<td>{{member}}</td>
				</tr>
			% end 
        </table>

	</body>    
</html>