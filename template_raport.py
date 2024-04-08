

template_heder = '''
    <style>
    table.GeneratedTable {
      width: 100%;
      background-color: #ffffff;
      border-collapse: collapse;
      border-width: 2px;
      border-color: #313335;
      border-style: solid;
      color: #000000;
    }

    table.GeneratedTable td, table.GeneratedTable th {
      border-width: 2px;
      border-color: #313335;
      border-style: solid;
      padding: 3px;
      
    }

    table.GeneratedTable thead {
      background-color: #ccc;
    }
    </style>

    <table class="GeneratedTable">
    <html>
    <head>
    <meta charset="UTF-8">
    </head>
    <title>Raport UPS</title>
    <body>  
      <thead>
      <p style="color:#ccc; padding: 0px; margin: 0px;">Developer: Dudko M.</p>
      <p style="color:#ccc; padding: 0px; margin: 0px;">Designed for: Petrikov, Republic Belarus \ Lic. key 775i</p>
      <p style="color:#ccc; padding: 0px; margin: 0px;">Developer contact: promsoft-1@ya.ru</p>
      <h3 style="padding-top: 20px;">Отчёт по ИБП</h3>
        <tr>
            <th>№<br></th>
            <th>Отделение<br></th>
            <th>Помещение</th>
            <th>Серийный №</th>
            <th>Инв.№</th>
            <th>Модель</th>
            <th>Тип корпуса</th>
            <th>Мощность(W)</th>
            <th>Тип АКБ(Ah\V)</th>
            <th>Кол. осн\доп.\Σ</th>
            <th>В работе</th>
            <th>Треб. зам.АКБ</th>
            <th>Дата замены</th>
            <th>В ремотне</th>
            <th>В ремонте с </th>
            <th>Дата ввода</th>
        </tr>
      </thead>
      <tbody>
    '''

template_bottom ='</tbody> </table><p>Итого: {}шт.</p><p>Дата создания: {}</p></body></html>'



