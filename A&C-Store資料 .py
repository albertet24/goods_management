import pymysql
conn= pymysql.connect(host="localhost", user="root", passwd="", db="a&c_store", charset="utf8" )
cur= conn.cursor()

from functools import partial
import pandas as pd
import tkinter as tk
#主程式
ac_store=tk.Tk()

ac_store.title("A&C商品管理系統")

ac_store.geometry("500x500")

ac_label=tk.Label(ac_store, text="A&C Store" ,font=1)
ac_label.pack(pady=20)

#商品資訊
def product ():
    product_page=tk.Toplevel()
    product_page.geometry("300x300")
    
    #管理下架商品
    def del_product():
        del_page=tk.Toplevel(bd=10)
        delet_sql="SELECT pro_pk, pro_name, pro_price, pro_stock FROM product WHERE pro_del ='1' "
        #print(delet_sql)
        cur.execute(delet_sql)
        del_list=cur.fetchall()
        
        num_sql = "SELECT pro_pk FROM product WHERE pro_del = '1'"
        cur.execute(num_sql)
        product_num = cur.fetchall()
        
        del_label = tk.Label(del_page, text="下架商品管理", font=1)
        del_label.pack()
        
        def pro_sale(stock_entry,sale_name):
            new_stock=stock_entry.get()
            sale_sql=f"UPDATE product SET pro_stock ='{new_stock}', pro_del='0' WHERE pro_name='{sale_name}'"
            cur.execute(sale_sql)
            conn.commit()
            
        
        def del_List():
            delet_list=len(product_num)
            for i in range(delet_list):
                del_info = del_list[i]
                sale_name= del_info[1]
                
                del_frame=tk.Frame(del_page,bd=5)
                del_frame.pack(anchor="w")
                name_label=tk.Label(del_frame, text=f"商品名稱: {del_info[1]}")
                name_label.pack(side="left", anchor="w")
                
                price_label=tk.Label(del_frame, text=f'商品價格: {del_info[2]}')
                price_label.pack(side="left", anchor='w')
                
                stock_label=tk.Label(del_frame, text="商品庫存: ")
                stock_entry=tk.Entry(del_frame)
                stock_entry.insert(0, del_info[3])
                stock_label.pack(side="left")
                stock_entry.pack(side="left")
                
                chk_btn=tk.Button(del_frame, text="上架", command=partial(pro_sale, stock_entry,sale_name))
                chk_btn.pack(padx=10,side="left")
                
                
        del_List()        
                
        def leave ():
            del_page.destroy()
        leave_btn=tk.Button(del_page, text="離開",command=leave)
        leave_btn.pack()
    
    
    def Product_info():
        new_page1 = tk.Toplevel(bd=10)
    
        search_sql = "SELECT pro_pk, pro_name, pro_price, pro_stock FROM product WHERE pro_del = '0'"
        cur.execute(search_sql)
        product_result = cur.fetchall()
    
        num_sql = "SELECT pro_pk FROM product WHERE pro_del = '0'"
        cur.execute(num_sql)
        product_num = cur.fetchall()
    
        
        info_frame = tk.Frame(new_page1, bd=10)
        info_label = tk.Label(info_frame, text="商品資料管理", font=1)
        info_frame.pack()
        info_label.pack()
    
        #更新商品按鈕 pro_change
        def pro_change(product_id, name_entry, price_entry, stock_entry):
            
            new_name=name_entry.get()
            new_price=price_entry.get()
            new_stock=stock_entry.get()
            change_sql = f"UPDATE product SET pro_name = '{new_name}', pro_price = '{new_price}', pro_stock = '{new_stock}' WHERE pro_pk = '{product_id}'"
            #print(change_sql)
            cur.execute(change_sql)
            conn.commit()

             
        
        def pro_list():
            
            product_list = len(product_num)  
            for i in range(product_list):
                product_info = product_result[i]
                product_frame = tk.Frame(info_frame,bd=10)
                product_frame.pack(anchor="w")
                product_id=product_info[0]
                
                pk_label=tk.Label(product_frame,text=f'{product_info[0]}. ')
                pk_label.pack(side="left", anchor="w")
                
                name_label=tk.Label(product_frame,text="品名 : ")
                name_label.pack(side="left", anchor="w")
                name_entry=tk.Entry(product_frame)
                name_entry.insert(0, product_info[1])#0是開始位置
                name_entry.pack(side="left",anchor="w")
                
                price_label=tk.Label(product_frame,text="價格 : ")
                price_label.pack(side="left", anchor="w")
                price_entry=tk.Entry(product_frame)
                price_entry.insert(0, product_info[2])#0是開始位置
                price_entry.pack(side="left",anchor='w' )
                
                stock_label=tk.Label(product_frame,text="庫存量 : ")
                stock_label.pack(side="left", anchor="w")
                stock_entry=tk.Entry(product_frame)
                stock_entry.insert(0, product_info[3])#0是開始位置
                stock_entry.pack(side="left",anchor="w")
                
                pro_btn=tk.Button(product_frame, text="修改", command=partial(pro_change,product_id,name_entry, price_entry,stock_entry))
                pro_btn.pack(side="left")
              

        pro_list()
        def leave ():
            new_page1.destroy()
        leave_btn=tk.Button(new_page1, text="離開",command=leave)
        leave_btn.pack()
        
        
    
    def New_product():
        def back_index():
            new_page.destroy()
            
        def keyin_info():
            try:
                pro_name= list_entry1.get()
                pro_price=int(list_entry2.get())
                pro_stock=int( list_entry3.get())
                result_sql="INSERT INTO product (pro_name, pro_price, pro_stock) VALUES  ('%s', %s , %s) "
                values=(pro_name, pro_price, pro_stock)
                #print(result_sql % values)
                cur.execute(result_sql % values)
                conn.commit()
                result_label.config(text=f'{pro_name}價格: {pro_price}，庫存量{pro_stock}')
                return_btn=tk.Button(result_frame, text="返回選單",command=back_index)
                return_btn.pack()
                
            except ValueError:
                result_label.config(text='金額和庫存請輸入數字')
            
        new_page=tk.Toplevel(product_page)
        list_frame1=tk.Frame(new_page,bd=10)
        list_label1=tk.Label(list_frame1,text="請輸入商品名稱: ")
        list_entry1=tk.Entry(list_frame1)
        list_frame1.pack(side="top", anchor=tk.CENTER)
        list_label1.pack(side="left")
        list_entry1.pack(side="left")
        
        list_frame2=tk.Frame(new_page,bd=10)
        list_label2=tk.Label(list_frame2,text="請輸入商品金額: ")
        list_entry2=tk.Entry(list_frame2)
        list_frame2.pack(side="top", anchor=tk.CENTER)
        list_label2.pack(side="left")
        list_entry2.pack(side="left")
        
        list_frame3=tk.Frame(new_page,bd=10)
        list_label3=tk.Label(list_frame3,text="請輸入商品庫存: ")
        list_entry3=tk.Entry(list_frame3)
        list_frame3.pack(side="top", anchor=tk.CENTER)
        list_label3.pack(side="left")
        list_entry3.pack(side="left")
        
        
        list_btn=tk.Button(new_page, text="確認", command=keyin_info)
        list_btn.pack(padx=5)
        
        result_frame=tk.Frame(new_page,bd=10)
        result_label=tk.Label(result_frame,text="")
        result_frame.pack(padx=10, pady=10, anchor="w", )
        result_label.pack()
        
    ac_list_btn1= tk.Button(product_page, text='1. 新商品登入', command=New_product)
    ac_list_btn2= tk.Button(product_page, text='2. 商品資料管理' , command= Product_info)
    ac_list_btn3= tk.Button(product_page, text='3. 未上架商品資料',command=del_product)
    ac_list_btn1.pack(pady=20)
    ac_list_btn2.pack(pady=20)
    ac_list_btn3.pack(pady=20)
#會員管理系統
def VIP ():
    
    def search():
        search_acc= search_entry.get()
        search_sql="SELECT mr_pk ,mr_account, mr_name, mr_phone, mr_address FROM member WHERE mr_name LIKE '%"+search_acc+"%' AND mr_del='0' "
        #print(search_sql)
        cur.execute(search_sql)
        search_result= cur.fetchall()
        num_sql="SELECT mr_pk FROM member WHERE mr_name LIKE '%"+search_acc+"%' AND mr_del='0' "
        #print(num_sql)
        cur.execute(num_sql)
        num_result=cur.fetchall()
        
        def acc_change (acc_id,name_entry, phone_entry,address_entry):
                new_name=name_entry.get()
                new_phone=phone_entry.get()
                new_add=address_entry.get()
                change_sql = 'UPDATE member SET mr_name=%s, mr_phone=%s, mr_address=%s WHERE mr_pk=%s'
                cur.execute(change_sql, (new_name, new_phone, new_add, acc_id))
                conn.commit()
        for widget in list_frame.winfo_children():
            widget.destroy()
            
        if not search_result:
            tk.Label(list_frame, text="未找到結果").pack(anchor="w")
            return
                
        else:    
            acc_num=len(num_result)
            #print(acc_num)
            for i in range(acc_num):
                
                search_list=search_result[i]
                acc_id=search_list[0]
                
                acc_frame=tk.Frame(list_frame, bd=10)
                acc_frame.pack(anchor="w")
                pk_label=tk.Label(acc_frame,text=f'{acc_id}. ')
                pk_label.pack(side="left", anchor="w")
                
                name_label=tk.Label(acc_frame,text="姓名 : ")
                name_label.pack(side="left", anchor="w")
                name_entry=tk.Entry(acc_frame)
                name_entry.insert(0, search_list[2])#0是開始位置
                name_entry.pack(side="left",anchor="w")
                
                phone_label=tk.Label(acc_frame,text="電話 : ")
                phone_label.pack(side="left", anchor="w")
                phone_entry=tk.Entry(acc_frame)
                phone_entry.insert(0, search_list[3])#0是開始位置
                phone_entry.pack(side="left",anchor='w' )
                
                address_label=tk.Label(acc_frame,text="地址 : ")
                address_label.pack(side="left", anchor="w")
                address_entry=tk.Entry(acc_frame)
                address_entry.insert(0, search_list[4])#0是開始位置
                address_entry.pack(side="left",anchor="w")
                
                pro_btn=tk.Button(acc_frame, text="修改", command = partial(acc_change, acc_id, name_entry, phone_entry, address_entry))
                pro_btn.pack(side="left")
        
    vip_page=tk.Toplevel()
    search_frame=tk.Frame(vip_page,bd=10)
    search_frame.pack(anchor="w")
    search_label=tk.Label(search_frame, text="查詢帳號: ")
    search_entry=tk.Entry(search_frame)
    search_btn=tk.Button(search_frame, text="查詢", command=search)
    search_label.pack(side="left")
    search_entry.pack(side="left")
    search_btn.pack(side="left",padx=10)
    
    list_frame=tk.Frame(vip_page,bd=10)
    list_frame.pack(anchor="w")
    
def Order():
    new_page2 = tk.Toplevel()
    title1_frame=tk.Frame(new_page2, bd=10)
    title1_frame.pack()
    title_label=tk.Label(title1_frame, text="訂單資料管理", font=1)
    title_label.pack()
    
    search_order="SELECT * FROM orders WHERE create_time >= 'start_time' AND createtime <='end_time' "
    
    search_frame=tk.Frame(new_page2, bd=20)
    search_frame.pack()
    type_label=tk.Label(search_frame,text="依條件搜尋: ")
    type_label.pack(side="left", anchor="w")
    
    condition = ["1. 日期","2. 帳號", "3. 商品"]
    co_vars = [tk.BooleanVar() for _ in range(len(condition))]
    for i in range (len(condition)):
        condition_box = tk.Checkbutton(search_frame, text=condition[i], variable=co_vars[i]])
    
    click_frame = tk.Frame(new_page2, bd=5)
    click_frame.pack()
    year_list=list(range(2014,2025))
    year_value=tk.StringVar()
    year_value.set("2024")
    year = tk.OptionMenu(click_frame, year_value, *year_list)
    year.pack(side="left", anchor="w")
    
    month_list=list(range(1,13))
    month_value=tk.StringVar()
    month_value.set("1")
    month = tk.OptionMenu(click_frame, month_value, *month_list)
    month.pack(side="left", anchor="w")
    
    day_list = list(range(1, 32))
    day_value = tk.StringVar()
    day_value.set("1")
    day = tk.OptionMenu(click_frame, day_value, *day_list)
    day.pack(side='left', anchor='w')
    
    type_btn1=tk.Button(new_page2, text="搜尋")
    type_btn1.pack(pady=10)
    
    

ac_list_btn1= tk.Button(ac_store, text='1. 商品資訊管理', command=product)
ac_list_btn2= tk.Button(ac_store, text='2. 會員資料管理' , command=VIP)
ac_list_btn3= tk.Button(ac_store, text='3. 訂單資料管理', command=Order)
ac_list_btn4= tk.Button(ac_store, text='4. 支付方式管理')
ac_list_btn1.pack(pady=20)
ac_list_btn2.pack(pady=20)
ac_list_btn3.pack(pady=20)
ac_list_btn4.pack(pady=20)


ac_store.mainloop()