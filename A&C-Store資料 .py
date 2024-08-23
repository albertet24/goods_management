import pymysql
conn= pymysql.connect(host="localhost", user="root", passwd="", db="a&c_store", charset="utf8" )
cur= conn.cursor()

from functools import partial

import tkinter as tk
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
        
        def del_List():
            delet_list=len(product_num)
            for i in range(delet_list):
                del_info = del_list[i]
        
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
                
                chk_btn=tk.Button(del_frame, text="上架")
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
    

ac_list_btn1= tk.Button(ac_store, text='1. 商品資訊管理', command=product)
ac_list_btn2= tk.Button(ac_store, text='2. 會員資料管理')
ac_list_btn3= tk.Button(ac_store, text='3. 訂單資料管理')
ac_list_btn4= tk.Button(ac_store, text='4. 支付方式管理')
ac_list_btn1.pack(pady=20)
ac_list_btn2.pack(pady=20)
ac_list_btn3.pack(pady=20)
ac_list_btn4.pack(pady=20)


ac_store.mainloop()