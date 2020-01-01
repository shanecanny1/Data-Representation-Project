import mysql.connector

class ProjectDAO:
    db=""
    def __init__(self): 
        self.db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        port=3308,
        database="project"
        )
    
            
    def create(self, values):
        cursor = self.db.cursor()
        sql="insert into movies (ChartNo, Title, Director, Budget, BoxOffice, RunningTimeMinutes) values (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, values)

        self.db.commit()
        return cursor.lastrowid

    def getAll(self):
        cursor = self.db.cursor()
        sql="select * from movies"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
        print(results)
        for result in results:
            print(result)
            returnArray.append(self.convertToDictionary(result))

        return returnArray

    def findByID(self, ChartNo):
        cursor = self.db.cursor()
        sql="SELECT * from movies WHERE ChartNo = %s"
        values=(ChartNo,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        return self.convertToDictionary(result)

    def update(self, values):
        cursor = self.db.cursor()
        sql="update movies set Title=%s,Director=%s,Budget=%s,BoxOffice=%s,RunningTimeMinutes=%s where ChartNo = %s"
        cursor.execute(sql, values)
        self.db.commit()

    def delete(self, ChartNo):
        cursor = self.db.cursor()
        sql="delete from movies where ChartNo = %s"
        values = (ChartNo,)

        cursor.execute(sql, values)

        self.db.commit()
        print("delete done")

    def convertToDictionary(self, result):
        colnames=['ChartNo','Title','Director', 'Budget','BoxOffice',"RunningTimeMinutes"]
        item = {}
        
        if result:
            for i, colName in enumerate(colnames):
                value = result[i]
                item[colName] = value
        
        return item
        
projectDAO = ProjectDAO()