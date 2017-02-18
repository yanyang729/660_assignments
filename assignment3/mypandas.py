from collections import OrderedDict
import csv
from dateutil.parser import parse
import datetime,time
import copy

class DataFrame(object):
    @classmethod
    def from_csv(cls,path):
        with open(path,'rU') as f:
            reader =csv.reader(f,delimiter=',',quotechar='"')
            data = []
            for row in reader:
                data.append(row)
        return cls(data)

    def __init__(self,list_of_lists,header=True):
        if header:
            self.data = list_of_lists[1:]
            self.header = list_of_lists[0]
            if len(set(self.header)) != len(self.header):
                raise Exception('duplicates found')
        else:
            self.header = ['column' + str(i+1) for i in range(len(list_of_lists[0]))]
            self.data = list_of_lists


        # =============change str values to appropriate data type=================
        def data_prep(row):
            for i in range(len(row)):
                try:
                    # if str is numeric, change to float
                    row[i] = float(row[i].replace(',',''))
                except:
                    try:
                        # if str is date, change to datetime
                        row[i] = datetime.datetime.strptime(row[i],'%m/%d/%y %H:%M')
                    except:
                        try:
                            # if string, strip blank
                            row[i] = row[i].strip()
                        except:
                            # otherwise, leave it as it is
                            pass
            return row

        self.data = [data_prep(row) for row in self.data]
        self.data = [OrderedDict(zip(self.header,row)) for row in self.data]



    def __getitem__(self, item):
        if isinstance(item,(int,slice)):
            return self.data[item]

        elif isinstance(item,str):
            return Series([row[item] for row in self.data])

        elif isinstance(item,tuple):
            if isinstance(item[0],list) or isinstance(item[1],list):
                if isinstance(item[0],list):
                    rowz = [row for index,row in enumerate(self.data) if index in item[0]]
                else:
                    rowz = self.data[item[0]]

                if isinstance(item[1],list):
                    if all([isinstance(i,int) for i in item[1]]):
                        return [[column_value for index,column_value in enumerate(row.values()) if index in item[1]] for row in rowz]
                    elif all([isinstance(i,str) for i in item[1]]):
                        return [[row[col] for col in item[1]] for row in rowz]
                    else:
                        raise TypeError('type error')

                else:
                    return rowz[item[1]]

            else:
                if isinstance(item[0],(int,slice)) and isinstance(item[1],(int,slice)):
                    return [list(row.values())[item[1]] for row in self.data[item[0]]]
                elif isinstance(item[1],str):
                    return [row[item[1]] for row in self.data[item[0]]]
                else:
                    raise TypeError('type error')

        elif isinstance(item,list):
            # ===========task 2 part1============
            if isinstance(item[0],str):
                list_of_dict =[]
                for row in self.data:
                    row_dict =[]
                    for i in item:
                        row_dict.append((i,row[i]))
                    list_of_dict.append(OrderedDict(row_dict))
                return list_of_dict
                    # return[OrderedDict([ (key,value) for key ,value in row.items() if key in item]) for row in self.data]
            elif isinstance(item[0],bool):
                return [row for is_needed,row in zip(item,self.data) if is_needed== True]
            else:
                raise TypeError('type error')

    def transform_type(self,col_name):
        is_time = 0
        try:
            nums = [float(row[col_name].replace(',','')) for row in self.data]
            return nums, 1 if is_time else 0
        except:
            try:
                nums = [parse(row[col_name].replace(',','')) for row in self.data]
                nums= [time.mktime(num.timetuple()) for num in nums]
                is_time = 1
                return nums, 1 if is_time else 0
            except:
                raise TypeError('text values cannot be calculated')


    def min(self,col_name):
        nums ,is_time= self.transform_type(col_name)
        rslt = min(nums)
        return datetime.datetime.fromtimestamp(rslt) if is_time else rslt

    def max(self,col_name):
        nums, is_time = self.transform_type(col_name)
        rslt = max(nums)
        return datetime.datetime.fromtimestamp(rslt) if is_time else rslt

    def median(self,col_name):
        nums, is_time = self.transform_type(col_name)
        nums = sorted(nums)
        center = int(len(nums) / 2)
        if len(nums) % 2 == 0:
            rslt = sum(nums[center - 1:center + 1]) / 2.0
            return datetime.datetime.fromtimestamp(rslt) if is_time else rslt
        else:
            rslt = nums[center]
            return datetime.datetime.fromtimestamp(rslt) if is_time else rslt

    def mean(self,col_name):
        nums, is_time = self.transform_type(col_name)
        rslt = sum(nums)/len(nums)
        return datetime.datetime.fromtimestamp(rslt) if is_time else rslt

    def sum(self,col_name):
        nums,is_time = self.transform_type(col_name)
        return sum(nums)

    def std(self,col_name):
        nums ,is_time = self.transform_type(col_name)
        mean = sum(nums)/len(nums)
        return (sum([(num-mean)**2 for num in nums])/len(nums))**0.5

    def get_rows_where_column_has_value(self, column_name, value, index_only=False):
        if index_only:
            return [index for index, row_value in enumerate(self[column_name]) if row_value==value]
        else:
            return [row for row in self.data if row[column_name]==value]

    def add_rows(self,list_of_lists):
        col_count = len(self.header)
        if sum([len(row) == col_count for row in list_of_lists]) == len(list_of_lists):
            self.data = self.data + [OrderedDict(zip(self.header, row)) for row in list_of_lists]
            return self
        else:
            raise Exception('incorrect number of columns')

    def add_columns(self,list_of_values):
        if len(list_of_values)==len(self.data):
            added_headers = ['column'+str(len(self.header)+i+1) for i in range(len(list_of_values[0]))]
            self.header = self.header + added_headers
            self.data = [OrderedDict(zip(list(old_row.keys()) + added_headers,list(old_row.values()) + added_values))
                         for old_row, added_values in zip(self.data, list_of_values)]
            return self
        else:
            raise Exception('incorrect number of rows')


    # ===========task 1============
    def sort_by(self,col_name, reverse):
        if isinstance(col_name,str):
            self.data = sorted(self.data,key= lambda x:x[col_name],reverse=reverse)

        elif isinstance(col_name,list):
            # reverse the list to realize hierarchical sort
            for i,col in enumerate(col_name[::-1]):
                self.data = sorted(self.data, key=lambda x:x[col], reverse=reverse[len(col_name)-1-i])
            return self
        else:
            raise Exception('type error')
        return self

    # ===========task 3============
    def group_by(self,col_group,col_agg,agg_func):
        ret_list = []
        if isinstance(col_group,str) and isinstance(col_agg,str):
            ret_list.append([col_group,col_agg])
            for group_value in set(self[col_group].data): # loop each group
                group = self[self[col_group] == group_value] # get the group, every group has same group_value
                agged = agg_func([row[col_agg] for row in group]) # aggregate col_agg column
                ret_list.append([group_value,agged])
            return DataFrame(ret_list,header=True)

        elif isinstance(col_group,list) and isinstance(col_agg,str):
            ret_list.append(col_group + [col_agg])
            unique_combo = [list(x) for x in set(tuple(y.values()) for y in self[col_group])]
            for line in unique_combo:
                bool_index = [True] * len(self.data) # default
                for i in range(len(col_group)):
                    bool_index = bool_index and (self[col_group[i]] == line[i])
                group = self[bool_index]
                agged = agg_func([row[col_agg] for row in group])
                ret_list.append(line+[agged])
            return DataFrame(ret_list,header=True)
        else:
            raise Exception('other cases ')

    # create a copy used for testing
    def copy(self):
        return copy.deepcopy(self)

# ===========task 2 part2============
class Series(object):
    def __init__(self, list_of_values):
        self.data = list_of_values

    def __eq__(self, other):
        ret_list = []
        for item in self.data:
            ret_list.append(item==other)
        return ret_list

    def __lt__(self, other):
        ret_list = []
        for item in self.data:
            ret_list.append(item < other)
        return ret_list

    def __gt__(self, other):
        ret_list = []
        for item in self.data:
            ret_list.append(item > other)
        return ret_list

    def __ge__(self, other):
        ret_list = []
        for item in self.data:
            ret_list.append(item >= other)
        return ret_list

    def __le__(self, other):
        ret_list = []
        for item in self.data:
            ret_list.append(item <= other)
        return ret_list

def avg(list_of_values):
    return sum(list_of_values)/float(len(list_of_values))

def mymin(list_of_values):
    return min(list_of_values)


if __name__ == '__main__':
    df = DataFrame.from_csv('SalesJan2009.csv')
    test = df.copy()















