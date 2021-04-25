<html>
    % include('head.tpl')
    <body>
        % include('header.tpl')

        <h2>response for SQL request: </h2><br>
        <h2> {{sql_request}} </h2>
        <table style="width:100%">
        % for row in tpl_rows:
            <tr>
                % for el in row:
                    <td>{{el}}</td>
                % end
            </tr>
        % end 
        </table>
    </body>
</html>