import pandas as pd
import streamlit as st
import hydralit_components as hc
from random import choices


st.set_page_config(layout="wide")

def main():
    import streamlit as st
    from random import choices
    import pandas as pd

    st.image("https://i.im.ge/2022/08/08/FK2DxG.1656330114723.jpg")

    menu_data= [
    {'icon':"fas fa-home",'label': "Home"},
    {'icon':"fa fa-database",'label': "Raw Data Transformation"},
    {'icon':"fa fa-database",'label': "Data"},
    {'icon':"far fa-chart-bar",'label': "Data Visualization"},
    {'icon':"fa fa-code",'label': "Clustering Models"},
    {'icon':"fa fa-code",'label': "Chosen Model"},
    {'icon':"fas fa-laptop", 'label': 'Classifier'},
    {'icon':"fa fa-users", 'label': 'Social Network Analysis'}
    ]
    menu_id= hc.nav_bar(menu_definition= menu_data, first_select=0, sticky_nav=True, hide_streamlit_markers=False,
        override_theme= {'menu_background':'red', 'txc_active':'black'})#sticky_mode='sticky'







    if menu_id == "Home":

        st.markdown("<h1 style='text-align: center; color: red;'>Customer Segmentation: A Telecom Case</h1>", unsafe_allow_html=True)

        st.image("https://i.im.ge/2022/08/08/FWcl6P.3de8030e-794e-4f4b-a089-7d114389d24eMM-New-Logo.png")



    page_style= """
    <style>
    footer{
        visibility: visible;
        }
    footer:after{
        content: ' Mohamad Dbouk x Monty Mobile x MSBA';
        display:block;
        position:relative;
        color:red;
    }
    </style>"""
    st.markdown(page_style, unsafe_allow_html=True)


    page_style_2= """
    <style>
    header{
        visibility: visible;
        }
    header:after{
        
        display:block;
        position:relative;
        color:green;
    }
    </style>"""
    st.markdown(page_style_2, unsafe_allow_html=True)


    if menu_id == "Raw Data Transformation":
        st.markdown(f'<h1 style="color:#3914DC;font-size:24px;">{"Please upload the Calls dataset followed by the Recharge bill dataset, in the mentioned order"}</h1>', unsafe_allow_html=True)
        

        uploaded_data = st.file_uploader('Upload here', type='csv')
        if uploaded_data:
            df=uploaded_data
            df['callbegintimestr']=df['callbegintime']
            df['callbegintimestr']=df['callbegintimestr'].astype(str)
            df['call_id']=pd.factorize(df['callingpartynumber'] + df['calledpartynumber'] + df['callbegintimestr'])[0]
            df2=df.copy()
            df2 = df2.sort_values(['call_id','chargepartyindicator'], ascending =[True, True])
            df2.drop_duplicates(subset='call_id', keep = 'first', inplace = True)
            dfA = df2[df2['chargepartyindicator']==1]
            dfB = df2[df2['chargepartyindicator']==2]
            dfA.drop_duplicates(inplace= True)
            dfB.drop_duplicates(inplace=True)
            #calls initiated
            df_calls_A = dfA.groupby('callingpartynumber')['callingpartynumber'].count().sort_values(ascending=False).reset_index(name="Calls_initiated")
            df_calls_B = dfB.groupby('callingpartynumber')['callingpartynumber'].count().sort_values(ascending=False).reset_index(name="Calls_initiated")
            df_calls_A.rename(columns ={'callingpartynumber':'user'}, inplace = True)
            df_calls_B.rename(columns ={'callingpartynumber':'user'}, inplace = True)
            df_calls = pd.concat([df_calls_A,df_calls_B])
            df_calls.reset_index(drop = True,inplace = True)
            df_calls1 = df_calls.groupby('user')['Calls_initiated'].sum().sort_values(ascending=False).reset_index(name="Calls_initiated")
            #talk time
            df_duration_A = dfA.groupby('callingpartynumber')['callduration'].sum().sort_values(ascending=False).reset_index(name="talk_time")
            df_duration_B = dfB.groupby('callingpartynumber')['callduration'].sum().sort_values(ascending=False).reset_index(name="talk_time")
            df_duration_A.rename(columns ={'callingpartynumber':'user'}, inplace = True)
            df_duration_B.rename(columns ={'callingpartynumber':'user'}, inplace = True)
            df_duration = pd.concat([df_duration_A,df_duration_B])
            df_duration.reset_index(drop = True,inplace = True)
            df_duration1 = df_duration.groupby('user')['talk_time'].sum().sort_values(ascending=False).reset_index(name="talk_time")
            #deducted fees
            df_deducted_A= dfA.groupby("callingpartynumber")['normal_cost'].sum().sort_values(ascending= False).reset_index(name="total_deducted")
            df_deducted_B= dfB.groupby("calledpartynumber")['normal_cost'].sum().sort_values(ascending= False).reset_index(name="total_deducted")
            df_deducted_A.rename(columns ={'callingpartynumber':'user'}, inplace = True)
            df_deducted_B.rename(columns ={'calledpartynumber':'user'}, inplace = True)
            df_deducted = pd.concat([df_deducted_A,df_deducted_B])
            df_deducted.reset_index(drop = True,inplace = True)
            df_deducted1 = df_deducted.groupby('user')['total_deducted'].sum().sort_values(ascending=False).reset_index(name="total_deducted")
            #standing Balance
            df_sb_A =dfA[dfA.groupby('callingpartynumber').callbegintime.transform('max')==dfA.callbegintime]
            df_sb2_A = df_sb_A.groupby(['callingpartynumber','normal_balance_after_call'])['callbegintime'].agg(pd.Series.max).reset_index(name='latest_date')
            df_sb3_A = df_sb2_A.drop_duplicates(subset=['callingpartynumber'],keep='first')
            df_sb_B =dfB[dfB.groupby('callingpartynumber').callbegintime.transform('max')==dfB.callbegintime]
            df_sb2_B = df_sb_B.groupby(['callingpartynumber','normal_balance_after_call'])['callbegintime'].agg(pd.Series.max).reset_index(name='latest_date')
            df_sb3_B = df_sb2_B.drop_duplicates(subset=['callingpartynumber'],keep='first')
            df_sb3_A.rename(columns ={'callingpartynumber':'user'}, inplace = True)
            df_sb3_B.rename(columns ={'callingpartynumber':'user'}, inplace = True)
            df_sb3 = pd.concat([df_sb3_A,df_sb3_B])
            df_sb3.reset_index(drop = True,inplace = True)
            df_sb3 = df_sb3.sort_values(['user','latest_date'],ascending =[True, False])
            df_sb3.drop_duplicates(subset='user', keep = 'first', inplace = True)
            df_sb3.reset_index(drop=True, inplace = True)
            # frequent service type of user
            df_frequent_servicetype_A= dfA.groupby("callingpartynumber")['service_type'].agg(pd.Series.mode).reset_index(name="usual_service_type")
            df_frequent_servicetype_B= dfB.groupby("callingpartynumber")['service_type'].agg(pd.Series.mode).reset_index(name="usual_service_type")
            df_frequent_servicetype_A.rename(columns ={'callingpartynumber':'user'}, inplace = True)
            df_frequent_servicetype_B.rename(columns ={'callingpartynumber':'user'}, inplace = True)
            df_frequent_servicetype= pd.concat([df_frequent_servicetype_A,df_frequent_servicetype_B])
            df_frequent_servicetype.reset_index(drop = True,inplace = True)
            df_frequent_servicetype.drop_duplicates(subset='user', keep = 'first', inplace = True)
            df_frequent_servicetype.reset_index(drop = True,inplace = True)
            #total free duration used
            df_freesecs_A= dfA.groupby("callingpartynumber")['freechgtime'].sum().sort_values(ascending= False).reset_index(name="total_free_duration_used")
            df_freesecs_B= dfB.groupby("calledpartynumber")['freechgtime'].sum().sort_values(ascending= False).reset_index(name="total_free_duration_used")
            df_freesecs_A.rename(columns ={'callingpartynumber':'user'}, inplace = True)
            df_freesecs_B.rename(columns ={'calledpartynumber':'user'}, inplace = True)
            df_freesecs = pd.concat([df_freesecs_A, df_freesecs_B])
            df_freesecs.reset_index(drop = True,inplace = True)
            df_freesecs1 = df_freesecs.groupby("user")['total_free_duration_used'].sum().sort_values(ascending= False).reset_index(name="total_free_duration_used")
            #call fees
            df_airtime_A= dfA.groupby("callingpartynumber")['airtimefee'].sum().sort_values(ascending= False).reset_index(name="Tairtimefee")
            df_ldaccess_A= dfA.groupby("callingpartynumber")['ldaccessfee'].sum().sort_values(ascending= False).reset_index(name="Tldaccessfee")
            df_intercon_A = dfA.groupby("callingpartynumber")['interconfee'].sum().sort_values(ascending= False).reset_index(name="Tinterconfee")
            df_toll_A = dfA.groupby("callingpartynumber")['tollfee'].sum().sort_values(ascending= False).reset_index(name="Ttollfee")
            df_flat_A = dfA.groupby("callingpartynumber")['flatfee'].sum().sort_values(ascending= False).reset_index(name="Tflatfee")
            df_roaming_A = dfA.groupby("callingpartynumber")['roamingfee'].sum().sort_values(ascending= False).reset_index(name="Troamingfee")
            dfsA=[df_airtime_A, df_ldaccess_A, df_intercon_A, df_toll_A, df_flat_A, df_roaming_A]
            from functools import reduce
            feesdfA = reduce(lambda left, right: pd.merge(left, right, on =["callingpartynumber"],how ='outer'), dfsA)
            feesdfA['totalfees']=feesdfA['Tairtimefee'] + feesdfA['Tldaccessfee'] + feesdfA['Tinterconfee'] + feesdfA['Ttollfee'] + feesdfA['Tflatfee'] + feesdfA['Troamingfee']
            df_airtime_B= dfB.groupby("calledpartynumber")['airtimefee'].sum().sort_values(ascending= False).reset_index(name="Tairtimefee")
            df_ldaccess_B= dfB.groupby("calledpartynumber")['ldaccessfee'].sum().sort_values(ascending= False).reset_index(name="Tldaccessfee")
            df_intercon_B = dfB.groupby("calledpartynumber")['interconfee'].sum().sort_values(ascending= False).reset_index(name="Tinterconfee")
            df_toll_B = dfB.groupby("calledpartynumber")['tollfee'].sum().sort_values(ascending= False).reset_index(name="Ttollfee")
            df_flat_B = dfB.groupby("calledpartynumber")['flatfee'].sum().sort_values(ascending= False).reset_index(name="Tflatfee")
            df_roaming_B = dfB.groupby("calledpartynumber")['roamingfee'].sum().sort_values(ascending= False).reset_index(name="Troamingfee")
            dfsB=[df_airtime_B, df_ldaccess_B, df_intercon_B, df_toll_B, df_flat_B, df_roaming_B]
            from functools import reduce
            feesdfB = reduce(lambda left, right: pd.merge(left, right, on =["calledpartynumber"],how ='outer'), dfsB)
            feesdfB['totalfees']=feesdfB['Tairtimefee'] + feesdfB['Tldaccessfee'] + feesdfB['Tinterconfee'] + feesdfB['Ttollfee'] + feesdfB['Tflatfee'] + feesdfB['Troamingfee']
            feesdfA.rename(columns ={'callingpartynumber':'user'}, inplace = True)
            feesdfB.rename(columns ={'calledpartynumber':'user'}, inplace = True)
            feesdf = pd.concat([feesdfA,feesdfB])
            feesdf.reset_index(drop = True,inplace = True)
            feesdf1 = feesdf.groupby('user')['totalfees'].sum().sort_values(ascending= False).reset_index(name="totalfees")
            #Average waiting duration
            df_waiting_A= dfA.groupby("callingpartynumber")['waitduration'].agg(pd.Series.mean).reset_index(name="Average_waiting_duration")
            df_waiting_B= dfB.groupby("callingpartynumber")['waitduration'].agg(pd.Series.mean).reset_index(name="Average_waiting_duration")
            df_waiting_A.rename(columns ={'callingpartynumber':'user'}, inplace = True)
            df_waiting_B.rename(columns ={'callingpartynumber':'user'}, inplace = True)
            df_waiting= pd.concat([df_waiting_A,df_waiting_B])
            df_waiting.reset_index(drop = True,inplace = True)
            df_waiting1 = df_waiting.groupby('user')['Average_waiting_duration'].agg(pd.Series.mean).reset_index(name="Average_waiting_duration")
            #billable
            df_total_billable_A= dfA.groupby("callingpartynumber")['billable_minutes'].sum().sort_values(ascending= False).reset_index(name="billable_minutes")
            df_total_billable_B= dfB.groupby("calledpartynumber")['billable_minutes'].sum().sort_values(ascending= False).reset_index(name="billable_minutes")
            df_total_billable_A.rename(columns ={'callingpartynumber':'user'}, inplace = True)
            df_total_billable_B.rename(columns ={'calledpartynumber':'user'}, inplace = True)
            df_total_billable =pd.concat([df_total_billable_A,df_total_billable_B])
            df_total_billable.reset_index(drop = True,inplace = True)
            df_total_billable1 = df_total_billable.groupby('user')['billable_minutes'].sum().sort_values(ascending= False).reset_index(name="billable_minutes")
            #calls recieved
            df_calls_recieved_by_number_A= dfA.groupby('calledpartynumber')['calledpartynumber'].count().reset_index(name="calls_recieved_by_number")
            df_calls_recieved_by_number_B= dfB.groupby('calledpartynumber')['calledpartynumber'].count().reset_index(name="calls_recieved_by_number")
            df_calls_recieved_by_number_A.rename(columns ={'calledpartynumber':'user'}, inplace = True)
            df_calls_recieved_by_number_B.rename(columns ={'calledpartynumber':'user'}, inplace = True)
            df_calls_recieved_by_number =pd.concat([df_calls_recieved_by_number_A,df_calls_recieved_by_number_B])
            df_calls_recieved_by_number.reset_index(drop = True,inplace = True)
            df_calls_recieved_by_number1 = df_calls_recieved_by_number.groupby('user')['calls_recieved_by_number'].sum().sort_values(ascending= False).reset_index(name="calls_recieved_by_number")
            #usual call type
            df_calltypes_A = dfA.groupby("callingpartynumber")['calltype'].agg(pd.Series.mode).reset_index(name="usual_call_type")
            df_calltypes_B = dfB.groupby("callingpartynumber")['calltype'].agg(pd.Series.mode).reset_index(name="usual_call_type")
            df_calltypes_A.rename(columns ={'callingpartynumber':'user'}, inplace = True)
            df_calltypes_B.rename(columns ={'callingpartynumber':'user'}, inplace = True)
            df_calltypes=pd.concat([df_calltypes_A,df_calltypes_B])
            df_calltypes.reset_index(drop = True,inplace = True)
            df_calltypes.drop_duplicates(subset='user', keep = 'first', inplace = True)
            df_calltypes.reset_index(drop = True,inplace = True)
            #usual charge type
            df_chargetypes_A = dfA.groupby("callingpartynumber")['chargetype'].agg(pd.Series.mode).reset_index(name="usual_charge_type")
            df_chargetypes_B = dfB.groupby("callingpartynumber")['chargetype'].agg(pd.Series.mode).reset_index(name="usual_charge_type")
            df_chargetypes_A.rename(columns ={'callingpartynumber':'user'}, inplace = True)
            df_chargetypes_B.rename(columns ={'callingpartynumber':'user'}, inplace = True)
            df_chargetypes =pd.concat([df_chargetypes_A,df_chargetypes_B])
            df_chargetypes.reset_index(drop = True,inplace = True)
            df_chargetypes.drop_duplicates(subset='user', keep = 'first', inplace = True)
            df_chargetypes.reset_index(drop = True,inplace = True)
            #Termination reason
            df_Termination_reason_A= dfA.groupby("callingpartynumber")['terminationreason'].agg(pd.Series.mode).reset_index(name="usual_terminationreason")
            df_Termination_reason_B= dfB.groupby("callingpartynumber")['terminationreason'].agg(pd.Series.mode).reset_index(name="usual_terminationreason")
            df_Termination_reason_A.rename(columns ={'callingpartynumber':'user'}, inplace = True)
            df_Termination_reason_B.rename(columns ={'callingpartynumber':'user'}, inplace = True)
            df_Termination_reason=pd.concat([df_Termination_reason_A,df_Termination_reason_B])
            df_Termination_reason.reset_index(drop = True,inplace = True)
            df_Termination_reason.drop_duplicates(subset='user', keep = 'first', inplace = True)
            df_Termination_reason.reset_index(drop = True,inplace = True)
            #merging all
            dfcallsdf=[df_calls1,df_waiting1,feesdf1,df_freesecs1,df_frequent_servicetype,df_sb3,df_deducted1,df_duration1,df_calls_recieved_by_number1,df_total_billable1,df_calltypes,df_chargetypes,df_Termination_reason]
            from functools import reduce
            dfcallsdfnew = reduce(lambda left, right: pd.merge(left, right, on =["user"],how ='outer'), dfcallsdf)

            dfcallscheck = dfcallsdfnew.copy()
            df_agg_1 = dfcallscheck.dropna(subset=['Calls_initiated'])
            df_agg_1['calls_recieved_by_number'] = df_agg_1['calls_recieved_by_number'].fillna(0)
            df_agg_1.reset_index(drop = True,inplace = True)
            df_agg_1.fillna(0, inplace = True)


            #calls table done

            uploaded_data_2 = st.file_uploader('Upload dataset', type='csv')
            if uploaded_data_2:
                dfr = uploaded_data_2
                df3=dfr.drop(columns=['extravideominute','extrafreemms','extrafreevolume','extrafreeminute2','extrafreeminute3','extrafreesm2','extrafreesm3','rrmpoint','rechargetax'], axis=1)
                df_countrecharges = df3.groupby('md5')['md5'].count().reset_index(name="count_of_recharges")
                df_subscriberclass = df3.groupby('md5')['subscriberclassofservice'].agg(pd.Series.mode).reset_index(name="sub_class_service")
                df_facevalues = df3.groupby('md5')['facevalue'].sum().reset_index(name="sum_of_facevalue")
                df_rechargetype = df3.groupby('md5')['recharge_type'].agg(pd.Series.mode).reset_index(name="frequent_recharge_type")
                df_regecard = df3.groupby('md5')['regecardserviceclass'].agg(pd.Series.mode).reset_index(name="rege_card_serviceclass")
                dfrechargedfs=[df_countrecharges,df_subscriberclass,df_facevalues,df_rechargetype,df_regecard]
                from functools import reduce
                dfrechargedfsnew = reduce(lambda left, right: pd.merge(left, right, on =["md5"],how ='outer'), dfrechargedfs)
                dfrechargedfsnew.rename(columns={'md5':'user'},inplace = True)

                joint=[df_agg_1,dfrechargedfsnew]
                from functools import reduce
                df_All_1 = reduce(lambda left, right: pd.merge(left, right, on =["user"],how ='outer'), joint)

                dfA =df_All_1.dropna(subset=['count_of_recharges'])
                df_fullusers = dfA.dropna(subset=['Calls_initiated'])
                df_fullusers.reset_index(inplace = True)
                df_fullusers.drop(columns=['index'], axis=1, inplace = True)
                df_fu = df_fullusers.copy()
                df_fu['usual_service_type']=df_fu['usual_service_type'].replace([1,2,3,4,5,6],['PPS','FNS','Data Service','Special International Route','Volume Discount','UCB Service'])
                df_fu['usual_call_type']=df_fu['usual_call_type'].astype('str')
                df_fu['usual_call_type']=df_fu['usual_call_type'].replace(['0','1','2','3','4','5','6','7'],['On Net Mobile Calling','PSTN Calling','On Net Mobile Called','Off Net Mobile Calling','Off Net Mobile Called','USSD Calling','Group Calling','First Activation'])
                df_fu['usual_charge_type']=df_fu['usual_charge_type'].astype('str')
                df_fu['usual_charge_type']=df_fu['usual_charge_type'].replace(['0','1','2','3','4','5','6','7','8','9','10'],['International toll call','Domestic toll call','Local call','Called praty roaming','Charge-free call','Forwarding and charge to the calling party','Forwarding and charge to the called party','charge order of a forwarded voice mailbox','One-off charge','Non voice call','Incoming bonus call'])
                df_fu['usual_terminationreason']=df_fu['usual_terminationreason'].astype('str')
                df_fu['usual_terminationreason']=df_fu['usual_terminationreason'].replace(['1','2','3'],['on hook','Insufficient balance','Over maximum call duration'])
                df_fu['frequent_recharge_type'] = df_fu['frequent_recharge_type'].astype('str')
                df_fu['frequent_recharge_type'] =df_fu['frequent_recharge_type'].replace(['0','1','2','3','4'],['first activation','recharge by IVR','recharge by USSD','recharge by SMAP or MML','recharge by SMS'])
                df_fu['rege_card_serviceclass']=df_fu['rege_card_serviceclass'].astype(float)


                data = df_fu.copy()
                data['sub_class_service']=data['sub_class_service'].astype('str')
                data['sub_class_service']=data['sub_class_service'].replace(['1.0','5.0','6.0'],['class1','class5','class6'])
                data['rege_card_serviceclass']=data['rege_card_serviceclass'].astype('str')
                data['rege_card_serviceclass']=data['rege_card_serviceclass'].replace(['1.0'],['class1'])

                import streamlit as st
                @st.cache
                def convert_df(dataframe):
                    return dataframe.to_csv(index= False)

                csv_data= convert_df(data)
                st.download_button(label="Export new aggregated Data as CSV to apply algorithms on", data=csv_data, file_name='montyaggregated.csv', mime='text/csv')

        























    if menu_id == "Data":
        st.markdown(f'<h1 style="color:#3914DC;font-size:24px;">{"Please upload the downloaded data resulting from the transformation of the previous page"}</h1>', unsafe_allow_html=True)
        uploaded_data = st.file_uploader('Upload dataset', type='csv')
        if uploaded_data:
            st.markdown("<h1 style='text-align: center; color: red;'>Customer Specific Metrics, Unclustered</h1>", unsafe_allow_html=True)
            data= pd.read_csv(uploaded_data)
            with open('style1.css') as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
            Kpi1, Kpi2, Kpi3, Kpi4 =st.columns(4)

            col = data.columns
            Kpi1.metric(label ="Number of Features", value = len(col))

            Kpi2.metric(label="Number of Customers in Study", value = len(data))

            Kpi3.metric(label="Null values", value = data.isnull().sum().sum())

            Kpi4.metric(label="Duplicates", value =data.duplicated().sum().sum())


            usual_call_type=st.sidebar.multiselect("select Call type:",options=data["usual_call_type"].unique(),default= data["usual_call_type"].unique())
            usual_charge_type=st.sidebar.multiselect("select Charge type:",options=data["usual_charge_type"].unique(),default= data["usual_charge_type"].unique())
            usual_terminationreason=st.sidebar.multiselect("select termination Reason:",options=data["usual_terminationreason"].unique(),default= data["usual_terminationreason"].unique())

            df_selection = data.query("usual_call_type == @usual_call_type & usual_charge_type == @usual_charge_type & usual_terminationreason ==@usual_terminationreason")
            st.dataframe(df_selection,width=1200, height=300)

    
    if menu_id == "Data Visualization":
        uploaded_data = st.sidebar.file_uploader('Upload dataset', type='csv')
        if uploaded_data:

            from streamlit_option_menu import option_menu
            selected= option_menu(menu_title="Features", options=["Numerical","Categorical"],icons=['number','object'],orientation='horizontal')

            if selected =="Categorical":
            


                data=pd.read_csv(uploaded_data)
                col1, col2, col3,col4 = st.columns([1,1,1,1])

                with col1:
                    col = data.columns
                    theme_override = {'bgcolor': '#C8BFC4','title_color': '#0B0A0B', 'content_color': 'black', 'icon': 'fa fa-mobile', 'icon_color': 'Red'}
                    hc.info_card(title = 'CallTypes', content = data['usual_call_type'].nunique(),
                    theme_override=theme_override)
                with col2:
                    theme_override = {'bgcolor': '#C8BFC4','title_color': '#0B0A0B', 'content_color': '000000', 'icon': 'fa fa-assistive-listening-systems', 'icon_color': 'Red'}
                    hc.info_card(title = 'ChargeTypes', content = data['usual_charge_type'].nunique(),
                    theme_override=theme_override)
                with col3:
                    theme_override = {'bgcolor': '#C8BFC4','title_color': '#0B0A0B', 'content_color': '000000', 'icon': 'fa fa-times', 'icon_color': 'Red'}
                    hc.info_card(title = 'Termination', content = data['usual_terminationreason'].nunique(),
                    theme_override=theme_override)
                
                with col4:
                    theme_override = {'bgcolor': '#C8BFC4','title_color': '#0B0A0B', 'content_color': '000000', 'icon': 'fa fa-wrench', 'icon_color': 'Red'}
                    hc.info_card(title = 'ServiceTypes', content = data['usual_service_type'].nunique(),
                    theme_override=theme_override)

                b1, b2 = st.columns(2)
                from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
                import plotly.express as px
                import plotly.graph_objects as go
                import numpy as np
                with b1:
                    st.write("Usual call types distribution")
                    dfct = data.groupby('usual_call_type')['usual_call_type'].count().reset_index(name='counts')
                    fig10 = px.pie(dfct,values=dfct['counts'],names=dfct['usual_call_type'], color = dfct['usual_call_type'],color_discrete_map={'On Net Mobile Calling':'red',
                                 'Off Net Mobile Calling':'purple',
                                 'no usual type':'pink',
                                 'First Activation':'black','On Net Mobile Called':'gray'})
                    fig10=go.Figure(fig10)
                    b1.plotly_chart(fig10)


                with b2:
                    st.write("Usual termination reason distribution ")
                    dftr = data.groupby('usual_terminationreason')['usual_terminationreason'].count().reset_index(name='counts')
                    fig11 = px.pie(dftr,values=dftr['counts'],names=dftr['usual_terminationreason'], color = dftr['usual_terminationreason'],color_discrete_map={'Insufficient balance':'red',
                                 'no usual reason':'purple',
                                 'on hook':'pink',
                                 })
                    fig11=go.Figure(fig11)
                    b2.plotly_chart(fig11)

                c1, c2 = st.columns(2)
                with c1:
                    st.write("Usual charge types distribution")
                    dfcht = data.groupby('usual_charge_type')['usual_charge_type'].count().reset_index(name='counts')
                    fig12 = px.pie(dfcht,values=dfcht['counts'],names=dfcht['usual_charge_type'], color = dfcht['usual_charge_type'],color_discrete_map={'Charge-free call':'black',
                                 'Forwarding and charge to the calling party':'purple',
                                 'International toll call':'pink',
                                 'Local call':'red',
                                 'no usual type':'gray'
                                 })
                    fig12=go.Figure(fig12)
                    c1.plotly_chart(fig12)

                with c2:
                    st.write("Subscribers class of service distribution")
                    dfsc = data.groupby('sub_class_service')['sub_class_service'].count().reset_index(name='counts')
                    fig13 = px.pie(dfsc,values=dfsc['counts'],names=dfsc['sub_class_service'], color = dfsc['sub_class_service'],color_discrete_map={'class1':'red',
                                 'class5':'purple',
                                 'class6':'pink',
                                 
                                 
                                 })
                    fig13=go.Figure(fig13)
                    c2.plotly_chart(fig13)
            


            if selected =="Numerical":
                
                data= pd.read_csv(uploaded_data)

                from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
                import plotly.express as px
                import plotly.graph_objects as go
                import numpy as np
                

                import pandas_profiling

                from pandas_profiling import ProfileReport

                from streamlit_pandas_profiling import st_profile_report

                profile = ProfileReport(data,explorative= True)
			    
                st_profile_report(profile)



    if menu_id == "Clustering Models":

        uploaded_data = st.sidebar.file_uploader('Upload dataset', type='csv')
        if uploaded_data:
            data=pd.read_csv(uploaded_data)

        

            from streamlit_option_menu import option_menu

            selected= option_menu(menu_title="Models", options=["model 1","model 2","model 3","model 4","model 5","model 6","model 7"]
		    ,orientation='horizontal')

            import os
            import numpy as np 
            import pandas as pd
            from matplotlib import pyplot as plt
            import seaborn as sns
        
        
            from sklearn.tree import DecisionTreeClassifier
            from sklearn.model_selection import train_test_split
            from sklearn.metrics import r2_score, explained_variance_score, confusion_matrix, accuracy_score, classification_report, log_loss
            from math import sqrt
            from sklearn.preprocessing import StandardScaler
            from sklearn.cluster import KMeans, k_means

            if selected=="model 1":
                st.markdown("<h1 style='text-align: center; color: red;'>K means with all features and standard scaling</h1>", unsafe_allow_html=True)
                cols_use = data[['Calls_initiated', 'Average_waiting_duration',
       'totalfees', 'total_free_duration_used', 'usual_service_type',
       'normal_balance_after_call', 'total_deducted',
       'talk_time', 'calls_recieved_by_number', 'billable_minutes',
       'usual_call_type', 'usual_charge_type', 'usual_terminationreason',
       'count_of_recharges', 'sub_class_service', 'sum_of_facevalue',
       'frequent_recharge_type', 'rege_card_serviceclass']]
                encoded_cols_use = pd.get_dummies(cols_use)
                enc_sc_cols_use = StandardScaler().fit_transform(encoded_cols_use.values)
                enc_sc_cols_use_df = pd.DataFrame(enc_sc_cols_use,index=encoded_cols_use.index, columns = encoded_cols_use.columns)
                X_train = enc_sc_cols_use_df.values

                
                
                no_of_clusters = range(2,30)
                inertia = []


                for f in no_of_clusters:
                    kmeans = KMeans(n_clusters=f, random_state=222)
                    kmeans = kmeans.fit(X_train)
                    u = kmeans.inertia_
                    inertia.append(u)
                
                
                
                
                
                fig, (ax1) = plt.subplots(1, figsize=(12,6))
                xx = np.arange(len(no_of_clusters))
                ax1.plot(xx, inertia)
                ax1.set_xticks(xx)
                ax1.set_xticklabels(no_of_clusters, rotation='vertical')
                plt.xlabel('Number of clusters')
                plt.ylabel('Inertia Score')
                plt.title("Inertia Plot per k")
                with st.expander("K Selection - Elbow method"):
                    st.write("Getting the best number of clusters Using Inertia and Elbow method")
                    st.pyplot(fig)

                kmeans13 = KMeans(n_clusters=13, random_state=2)
                kmeans13 = kmeans13.fit(X_train)




                # "predictions" for new data
                predictions13 = kmeans13.predict(X_train)

                # calculating the Counts of the cluster
                unique13, counts13 = np.unique(predictions13, return_counts=True)
                counts13 = counts13.reshape(1,13)

                # Creating a datagrame
                countscldf13 = pd.DataFrame(counts13, columns = ["Cluster 0","Cluster 1","Cluster 2", "Cluster 3","Cluster 4","Cluster 5","Cluster 6","Cluster 7","Cluster 8","Cluster 9","Cluster 10","Cluster 11","Cluster 12"])

                # display
                with st.expander("Resulting clusters"):
                    st.dataframe(countscldf13)    
                
                st.set_option('deprecation.showPyplotGlobalUse', False)
                from sklearn.decomposition import PCA
                from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

                X = X_train
                y_num = predictions13


                target_names = ["Cluster 0","Cluster 1","Cluster 2", "Cluster 3","Cluster 4","Cluster 5","Cluster 6","Cluster 7","Cluster 8","Cluster 9","Cluster 10","Cluster 11","Cluster 12"]

                pca = PCA(n_components=2, random_state = 111)
                X_r = pca.fit(X).transform(X)




                plt.figure()
                plt.figure(figsize=(12,6))
                colors = ['navy', 'turquoise', 'darkorange', 'red', 'black','yellow','blue','green','pink','purple','brown','black','white']
                lw = 2


                for color, i, target_name in zip(colors, [0, 1, 2, 3, 4,5,6,7,8,9,10,11,12,13], target_names):
                    plt.scatter(X_r[y_num == i, 0], X_r[y_num == i, 1], color=color, alpha=.8, lw=lw,label=target_name)


                plt.legend(loc='best', shadow=False, scatterpoints=1)
                plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.6)   
                plt.title('PCA of 2 Components')
                with st.expander("PCA with 2 components explaining 28% of variance"):
                    st.pyplot()

                
                
                X11=enc_sc_cols_use_df.values
                n_components = X11.shape[1]

                # Running PCA with all components
                pca11 = PCA(n_components=n_components, random_state = 111)
                X_r_11 = pca11.fit(X11).transform(X11)


                # Calculating the 95% Variance
                total_variance = sum(pca11.explained_variance_)
                print("Total Variance in our dataset is: ", total_variance)
                var_95 = total_variance * 0.95

                    




                # Creating a df with the components and explained variance
                a11 = zip(range(0,n_components), pca11.explained_variance_)
                a11 = pd.DataFrame(a11, columns=["PCA Comp", "Explained Variance"])
# Trying to hit 95%
                (sum(a11["Explained Variance"][0:1]))
                sum(a11["Explained Variance"][0:2])
                sum(a11["Explained Variance"][0:3])
                sum(a11["Explained Variance"][0:5])
                sum(a11["Explained Variance"][0:8])
                sum(a11["Explained Variance"][0:11])
                sum(a11["Explained Variance"][0:15])
                sum(a11["Explained Variance"][0:18])
                sum(a11["Explained Variance"][0:19])
                sum(a11["Explained Variance"][0:22])
                sum(a11["Explained Variance"][0:24])


                sum(a11["Explained Variance"][0:28])








                # Plotting the Data
                plt.figure(1, figsize=(12, 6))
                plt.plot(pca11.explained_variance_ratio_, linewidth=2, c="r")
                plt.xlabel('n_components')
                plt.ylabel('explained_ratio_')

                # Plotting line with 95% e.v.
                plt.axvline(19,linestyle=':', label='n_components - 95% explained', c ="blue")
                plt.legend(prop=dict(size=12))

                # adding arrow
                plt.annotate('19 eigenvectors used to explain 95% variance', xy=(19, pca11.explained_variance_ratio_[19]), 
                xytext=(19, pca11.explained_variance_ratio_[19]),
                arrowprops=dict(facecolor='blue', shrink=0.05))
                
                with st.expander("Getting PCA component to reach 95% variance"):
                    html_string3="""<a href="https://im.ge/i/OraKGa"><img src="https://i.im.ge/2022/08/14/OraKGa.Screenshot-2022-08-14-211813.png" alt="Screenshot 2022-08-14 211813" border="0"></a>"""
                    st.markdown(html_string3, unsafe_allow_html= True)

                pca = PCA(n_components=19, random_state = 111)
                X_r = pca.fit(X).transform(X)

                inertia = []

                #running Kmeans

                for f in no_of_clusters:
                    kmeans = KMeans(n_clusters=f, random_state=2)
                    kmeans = kmeans.fit(X_r)
                    u = kmeans.inertia_
                    inertia.append(u)
                    print("The innertia for :", f, "Clusters is:", u)

                # Creating the scree plot for Intertia - elbow method
                fig, (ax1) = plt.subplots(1, figsize=(12,6))
                xx = np.arange(len(no_of_clusters))
                ax1.plot(xx, inertia)
                ax1.set_xticks(xx)
                ax1.set_xticklabels(no_of_clusters, rotation='vertical')
                plt.xlabel('clusters')
                plt.ylabel('Inertia Score')
                plt.title("Inertia Plot per k")
                with st.expander("re-iterating kmeans to get best K with Data fitted on PCA 19"):   
                    st.pyplot()

                from sklearn import metrics
                from sklearn.metrics import davies_bouldin_score


                #rerunning with optimal pca and optimal K
                pca = PCA(n_components=19, random_state = 111)
                X_r = pca.fit(X).transform(X)

                # Running Kmeans with 6 Ks
                kmeans = KMeans(n_clusters=13, random_state=2)
                kmeans = kmeans.fit(X_r)

                clusters00 = kmeans.labels_

                with st.expander("Model Evaluation using 4 metrics"):
                    st.write("The Silhouette Score")
                    st.markdown((metrics.silhouette_score(X_r,clusters00)))
                    st.write("the davies bouldin score")
                    st.markdown((davies_bouldin_score(X_r,clusters00)))
                    st.write("the calinski harabasz index score")
                    st.markdown((metrics.calinski_harabasz_score(X_r,clusters00)))
                    st.write("The inertia")
                    st.markdown((kmeans.inertia_))
                
                


            if selected=="model 2":
                st.markdown("<h1 style='text-align: center; color: Blue;'> K means with numerical features only, standard scaler</h1>", unsafe_allow_html=True)
                cols_use = data[['Calls_initiated', 'Average_waiting_duration',
       'totalfees', 'total_free_duration_used', 'usual_service_type',
       'normal_balance_after_call', 'total_deducted',
       'talk_time', 'calls_recieved_by_number', 'billable_minutes',
       'usual_call_type', 'usual_charge_type', 'usual_terminationreason',
       'count_of_recharges', 'sub_class_service', 'sum_of_facevalue',
       'frequent_recharge_type', 'rege_card_serviceclass']]
                encoded_cols_use = pd.get_dummies(cols_use)
                enc_sc_cols_use = StandardScaler().fit_transform(encoded_cols_use.values)
                enc_sc_cols_use_df = pd.DataFrame(enc_sc_cols_use,index=encoded_cols_use.index, columns = encoded_cols_use.columns)






                num_sd =enc_sc_cols_use_df[['Calls_initiated', 'Average_waiting_duration', 'totalfees',
       'total_free_duration_used',
       'normal_balance_after_call', 'total_deducted',
       'talk_time', 'calls_recieved_by_number', 'billable_minutes',
       
       'count_of_recharges', 'sum_of_facevalue',
                ]]
                X_train_A = num_sd.values
                no_of_clusters = range(2,30)
                inertia = []


                for f in no_of_clusters:
                    kmeans = KMeans(n_clusters=f, random_state=222)
                    kmeans = kmeans.fit(X_train_A)
                    u = kmeans.inertia_
                    inertia.append(u)
                
                fig, (ax1) = plt.subplots(1, figsize=(16,6))
                xx = np.arange(len(no_of_clusters))
                ax1.plot(xx, inertia)
                ax1.set_xticks(xx)
                ax1.set_xticklabels(no_of_clusters, rotation='vertical')
                plt.xlabel('Number of clusters')
                plt.ylabel('Inertia Score')
                plt.title("Inertia Plot per k")
                with st.expander("K selection - Elbow method"):
                    st.pyplot()


                kmeansA = KMeans(n_clusters=7, random_state=2)
                kmeansA = kmeansA.fit(X_train_A)


                

                # "predictions" for new data
                predictionsA = kmeansA.predict(X_train_A)

                # calculating the Counts of the cluster
                uniqueA, countsA = np.unique(predictionsA, return_counts=True)
                countsA = countsA.reshape(1,7)

                # Creating a datagrame
                countscldfA = pd.DataFrame(countsA, columns = ["Cluster 0","Cluster 1","Cluster 2", "Cluster 3","Cluster 4","Cluster 5","Cluster 6"])

                # display
                with st.expander("resulting Clusters"):
                    st.dataframe(countscldfA)

                from sklearn.decomposition import PCA
                from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

                X_A = X_train_A
                y_num = predictionsA


                target_names = ["Cluster 0","Cluster 1","Cluster 2", "Cluster 3","Cluster 4","Cluster 5","Cluster 6"]

                pca = PCA(n_components=2, random_state = 111)
                X_r_A = pca.fit(X_A).transform(X_A)


                print('Explained variance ratio (first two components): %s' % str(pca.explained_variance_ratio_))


                plt.figure()
                plt.figure(figsize=(12,8))
                colors = ['navy', 'turquoise', 'darkorange', 'red', 'black','yellow','blue','green','pink','purple','brown','black','white']
                lw = 2


                for color, i, target_name in zip(colors, [0, 1, 2, 3, 4,5,6], target_names):
                    plt.scatter(X_r_A[y_num == i, 0], X_r_A[y_num == i, 1], color=color, alpha=.8, lw=lw,label=target_name)


                plt.legend(loc='best', shadow=False, scatterpoints=1)
                plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.6)   
                plt.title('PCA of 2 Components')
                with st.expander("PCA with 2 components explaining 69% of variance"):
                    st.pyplot()



                n_components = X_A.shape[1]

                # Running PCA with all components
                pca = PCA(n_components=n_components, random_state = 111)
                X_r_A = pca.fit(X_A).transform(X_A)


                # Calculating the 95% Variance
                total_variance = sum(pca.explained_variance_)
                print("Total Variance in our dataset is: ", total_variance)
                var_95 = total_variance * 0.95

                # Creating a df with the components and explained variance
                a = zip(range(0,n_components), pca.explained_variance_)
                a = pd.DataFrame(a, columns=["PCA Comp", "Explained Variance"])


                # Plotting the Data
                plt.figure(1, figsize=(14, 8))
                plt.plot(pca.explained_variance_ratio_, linewidth=2, c="r")
                plt.xlabel('n_components')
                plt.ylabel('explained_ratio_')

                # Plotting line with 95% e.v.
                plt.axvline(6,linestyle=':', label='n_components - 95% explained', c ="blue")
                plt.legend(prop=dict(size=12))

                # adding arrow
                plt.annotate('6 eigenvectors used to explain 95% variance', xy=(6, pca.explained_variance_ratio_[6]), 
                xytext=(6, pca.explained_variance_ratio_[6]),
                arrowprops=dict(facecolor='blue', shrink=0.05))
                with st.expander("Getting PCA component to hit 95% variance"):
                    st.pyplot()





                pca = PCA(n_components=6, random_state = 111)
                X_r_A = pca.fit(X_A).transform(X_A)

                inertia = []

                #running Kmeans

                for f in no_of_clusters:
                    kmeans = KMeans(n_clusters=f, random_state=2)
                    kmeans = kmeans.fit(X_r_A)
                    u = kmeans.inertia_
                    inertia.append(u)
                    print("The innertia for :", f, "Clusters is:", u)

                # Creating the scree plot for Intertia - elbow method
                fig, (ax1) = plt.subplots(1, figsize=(16,6))
                xx = np.arange(len(no_of_clusters))
                ax1.plot(xx, inertia)
                ax1.set_xticks(xx)
                ax1.set_xticklabels(no_of_clusters, rotation='vertical')
                plt.xlabel('n_components Value')
                plt.ylabel('Inertia Score')
                plt.title("Inertia Plot per k")
                with st.expander("re-iterating kmeans to get best K with Data fitted on PCA 6"):
                    st.pyplot()

                
                from sklearn import metrics
                from sklearn.metrics import davies_bouldin_score


                #rerunning with optimal pca and optimal K
                pca = PCA(n_components=6, random_state = 111)
                X_r_A = pca.fit(X_A).transform(X_A)

                # Running Kmeans with 7 Ks
                kmeans = KMeans(n_clusters=7, random_state=2)
                kmeans = kmeans.fit(X_r_A)

                clusters01 = kmeans.labels_
                with st.expander("Model evaluation"):
                    st.write("the silhouette score")
                    st.markdown(metrics.silhouette_score(X_r_A,clusters01))
                    st.write("the davies bouldin score")
                    st.markdown(davies_bouldin_score(X_r_A,clusters01))
                    st.write("the calinski harabasz score")
                    st.markdown(metrics.calinski_harabasz_score(X_r_A,clusters01))
                    st.write("the inertia")
                    st.markdown(kmeans.inertia_)






            if selected =="model 3":
                st.markdown("<h1 style='text-align: center; color: Red;'>K means with min-max scaler, all features</h1>", unsafe_allow_html=True)
                cols_use = data[['Calls_initiated', 'Average_waiting_duration',
       'totalfees', 'total_free_duration_used', 'usual_service_type',
       'normal_balance_after_call', 'total_deducted',
       'talk_time', 'calls_recieved_by_number', 'billable_minutes',
       'usual_call_type', 'usual_charge_type', 'usual_terminationreason',
       'count_of_recharges', 'sub_class_service', 'sum_of_facevalue',
       'frequent_recharge_type', 'rege_card_serviceclass']]
                encoded_cols_use = pd.get_dummies(cols_use)
                enc_sc_cols_use = StandardScaler().fit_transform(encoded_cols_use.values)
                enc_sc_cols_use_df = pd.DataFrame(enc_sc_cols_use,index=encoded_cols_use.index, columns = encoded_cols_use.columns)









                from sklearn.preprocessing import MinMaxScaler
                enc_mm_cols_use = MinMaxScaler().fit_transform(encoded_cols_use.values)
                enc_mm_cols_use_df = pd.DataFrame(enc_mm_cols_use,index=encoded_cols_use.index, columns = encoded_cols_use.columns)

                no_of_clusters = range(2,30)
                inertia = []

                X_train_3 = enc_mm_cols_use_df.values
                for f in no_of_clusters:
                    kmeans = KMeans(n_clusters=f, random_state=222)
                    kmeans = kmeans.fit(X_train_3)
                    u = kmeans.inertia_
                    inertia.append(u)

                fig, (ax1) = plt.subplots(1, figsize=(16,6))
                xx = np.arange(len(no_of_clusters))
                ax1.plot(xx, inertia)
                ax1.set_xticks(xx)
                ax1.set_xticklabels(no_of_clusters, rotation='vertical')
                plt.xlabel('Number of clusters')
                plt.ylabel('Inertia Score')
                plt.title("Inertia Plot per k")
                with st.expander("K selection - elbow method"):
                    st.pyplot()


                kmeansmm = KMeans(n_clusters=6, random_state=2)
                kmeansmm = kmeansmm.fit(X_train_3)




                # "predictions" for new data
                predictionsmm = kmeansmm.predict(X_train_3)

                # calculating the Counts of the cluster
                uniquemm, countsmm = np.unique(predictionsmm, return_counts=True)
                countsmm = countsmm.reshape(1,6)

                # Creating a datagrame
                countscldfmm = pd.DataFrame(countsmm, columns = ["Cluster 0","Cluster 1","Cluster 2", "Cluster 3","Cluster 4","Cluster 5"])

                # display
                with st.expander("resulting cluster"):
                    st.dataframe(countscldfmm)


                X_3 = X_train_3
                y_num = predictionsmm


                target_names = ["Cluster 0","Cluster 1","Cluster 2", "Cluster 3","Cluster 4","Cluster 5"]

                from sklearn.decomposition import PCA
                from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

                pca = PCA(n_components=2, random_state = 111)
                X_r_3 = pca.fit(X_3).transform(X_3)


                print('Explained variance ratio (first two components): %s' % str(pca.explained_variance_ratio_))


                plt.figure()
                plt.figure(figsize=(12,8))
                colors = ['navy', 'turquoise', 'darkorange', 'red', 'black','yellow']
                lw = 2


                for color, i, target_name in zip(colors, [0, 1, 2, 3, 4,5], target_names):
                    plt.scatter(X_r_3[y_num == i, 0], X_r_3[y_num == i, 1], color=color, alpha=.8, lw=lw,label=target_name)


                plt.legend(loc='best', shadow=False, scatterpoints=1)
                plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.6)   
                plt.title('PCA of 2 Components')
                with st.expander("PCA with 2 components explaining 60% of variance"):
                    st.pyplot()


                n_components = X_3.shape[1]

                # Running PCA with all components
                pca = PCA(n_components=n_components, random_state = 111)
                X_r_3 = pca.fit(X_3).transform(X_3)


                # Calculating the 95% Variance
                total_variance = sum(pca.explained_variance_)
                print("Total Variance in our dataset is: ", total_variance)
                var_95 = total_variance * 0.95
                print("The 95% variance we want to have is: ", var_95)
                print("")

                a = zip(range(0,n_components), pca.explained_variance_)
                a = pd.DataFrame(a, columns=["PCA Comp", "Explained Variance"])


                plt.figure(1, figsize=(14, 8))
                plt.plot(pca.explained_variance_ratio_, linewidth=2, c="r")
                plt.xlabel('n_components')
                plt.ylabel('explained_ratio_')

                # Plotting line with 95% e.v.
                plt.axvline(8,linestyle=':', label='n_components - 95% explained', c ="blue")
                plt.legend(prop=dict(size=12))

                # adding arrow
                plt.annotate('8 eigenvectors used to explain 95% variance', xy=(8, pca.explained_variance_ratio_[8]), 
             xytext=(8, pca.explained_variance_ratio_[8]),
            arrowprops=dict(facecolor='blue', shrink=0.05))
                with st.expander("Getting PCA component to hit 95% variance"):
                    st.pyplot()



                pca = PCA(n_components=8, random_state = 111)
                X_r_3 = pca.fit(X_3).transform(X_3)

                inertia = []

                #running Kmeans

                for f in no_of_clusters:
                    kmeans = KMeans(n_clusters=f, random_state=2)
                    kmeans = kmeans.fit(X_r_3)
                    u = kmeans.inertia_
                    inertia.append(u)
                    print("The innertia for :", f, "Clusters is:", u)

                # Creating the scree plot for Intertia - elbow method
                fig, (ax1) = plt.subplots(1, figsize=(16,6))
                xx = np.arange(len(no_of_clusters))
                ax1.plot(xx, inertia)
                ax1.set_xticks(xx)
                ax1.set_xticklabels(no_of_clusters, rotation='vertical')
                plt.xlabel('n_components Value')
                plt.ylabel('Inertia Score')
                plt.title("Inertia Plot per k")
                with st.expander("re-iterating K means with data fitted on PCA 8 components"):
                    st.pyplot()




                from sklearn import metrics
                from sklearn.metrics import davies_bouldin_score


                #rerunning with optimal pca and optimal K
                pca = PCA(n_components=8, random_state = 111)
                X_r_3 = pca.fit(X_3).transform(X_3)

                # Running Kmeans with 6 Ks
                kmeans = KMeans(n_clusters=6, random_state=2)
                kmeans = kmeans.fit(X_r_3)

                clusters02 = kmeans.labels_

                with st.expander("model evaluation"):
                    st.write("the silhouette score")
                    st.markdown(metrics.silhouette_score(X_r_3,clusters02))
                    st.write("the davies bouldin indexscore")
                    st.markdown(davies_bouldin_score(X_r_3,clusters02))
                    st.write("the calinski harabasz index score")
                    st.markdown(metrics.calinski_harabasz_score(X_r_3,clusters02))
                    st.markdown("The inertia")
                    st.markdown(kmeans.inertia_)

                



                


        if selected=="model 4":
            st.markdown("<h1 style='text-align: center; color: Red;'>K means min-max scaler numeric features only</h1>", unsafe_allow_html=True)
            
            cols_use = data[['Calls_initiated', 'Average_waiting_duration',
       'totalfees', 'total_free_duration_used', 'usual_service_type',
       'normal_balance_after_call', 'total_deducted',
       'talk_time', 'calls_recieved_by_number', 'billable_minutes',
       'usual_call_type', 'usual_charge_type', 'usual_terminationreason',
       'count_of_recharges', 'sub_class_service', 'sum_of_facevalue',
       'frequent_recharge_type', 'rege_card_serviceclass']]
            encoded_cols_use = pd.get_dummies(cols_use)
            enc_sc_cols_use = StandardScaler().fit_transform(encoded_cols_use.values)
            enc_sc_cols_use_df = pd.DataFrame(enc_sc_cols_use,index=encoded_cols_use.index, columns = encoded_cols_use.columns)









            from sklearn.preprocessing import MinMaxScaler
            enc_mm_cols_use = MinMaxScaler().fit_transform(encoded_cols_use.values)
            enc_mm_cols_use_df = pd.DataFrame(enc_mm_cols_use,index=encoded_cols_use.index, columns = encoded_cols_use.columns)



            num_mm =enc_mm_cols_use_df[['Calls_initiated', 'Average_waiting_duration', 'totalfees',
       'total_free_duration_used',
       'normal_balance_after_call', 'total_deducted',
       'talk_time', 'calls_recieved_by_number', 'billable_minutes',
       
       'count_of_recharges', 'sum_of_facevalue']]

            X_train_B = num_mm.values
            no_of_clusters = range(2,30)
            inertia = []


            for f in no_of_clusters:
                kmeans = KMeans(n_clusters=f, random_state=222)
                kmeans = kmeans.fit(X_train_B)
                u = kmeans.inertia_
                inertia.append(u)
            

            fig, (ax1) = plt.subplots(1, figsize=(16,6))
            xx = np.arange(len(no_of_clusters))
            ax1.plot(xx, inertia)
            ax1.set_xticks(xx)
            ax1.set_xticklabels(no_of_clusters, rotation='vertical')
            plt.xlabel('Number of clusters')
            plt.ylabel('Inertia Score')
            plt.title("Inertia Plot per k")
            with st.expander("k selection - elbow method"):
                st.pyplot()


            kmeansB = KMeans(n_clusters=5, random_state=2)
            kmeansB = kmeansB.fit(X_train_B)


            

            # "predictions" for new data
            predictionsB = kmeansB.predict(X_train_B)

            # calculating the Counts of the cluster
            uniqueB, countsB = np.unique(predictionsB, return_counts=True)
            countsB = countsB.reshape(1,5)

            # Creating a datagrame
            countscldfB = pd.DataFrame(countsB, columns = ["Cluster 0","Cluster 1","Cluster 2", "Cluster 3","Cluster 4"])

            # display
            with st.expander("resulting clusters"):
                st.dataframe(countscldfB)

            from sklearn.decomposition import PCA
            from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

            X_B = X_train_B
            y_num = predictionsB


            target_names = ["Cluster 0","Cluster 1","Cluster 2", "Cluster 3","Cluster 4"]

            pca = PCA(n_components=2, random_state = 111)
            X_r_B = pca.fit(X_B).transform(X_B)


            print('Explained variance ratio (first two components): %s' % str(pca.explained_variance_ratio_))


            plt.figure()
            plt.figure(figsize=(12,8))
            colors = ['navy', 'turquoise', 'darkorange', 'red', 'black']
            lw = 2


            for color, i, target_name in zip(colors, [0, 1, 2, 3, 4], target_names):
                plt.scatter(X_r_B[y_num == i, 0], X_r_B[y_num == i, 1], color=color, alpha=.8, lw=lw,label=target_name)


            plt.legend(loc='best', shadow=False, scatterpoints=1)
            plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.6)   
            plt.title('PCA of 2 Components')
            with st.expander("PCA with 2 components explaining 83% of variance"):
                st.pyplot()


            n_components = X_B.shape[1]

            # Running PCA with all components
            pca = PCA(n_components=n_components, random_state = 111)
            X_r_B = pca.fit(X_B).transform(X_B)


            # Calculating the 95% Variance
            total_variance = sum(pca.explained_variance_)
            print("Total Variance in our dataset is: ", total_variance)
            var_95 = total_variance * 0.95
            print("The 95% variance we want to have is: ", var_95)
            print("")

            a = zip(range(0,n_components), pca.explained_variance_)
            a = pd.DataFrame(a, columns=["PCA Comp", "Explained Variance"])

            # Plotting the Data
            plt.figure(1, figsize=(14, 8))
            plt.plot(pca.explained_variance_ratio_, linewidth=2, c="r")
            plt.xlabel('n_components')
            plt.ylabel('explained_ratio_')

            # Plotting line with 95% e.v.
            plt.axvline(5,linestyle=':', label='n_components - 95% explained', c ="blue")
            plt.legend(prop=dict(size=12))

# adding arrow
            plt.annotate('5 eigenvectors used to explain 95% variance', xy=(5, pca.explained_variance_ratio_[5]), 
             xytext=(5, pca.explained_variance_ratio_[8]),
            arrowprops=dict(facecolor='blue', shrink=0.05))

            with st.expander("Getting PCA component to hit 95% variance"):

                st.pyplot()


            pca = PCA(n_components=5, random_state = 111)
            X_r_B = pca.fit(X_B).transform(X_B)

            inertia = []

            #running Kmeans

            for f in no_of_clusters:
                kmeans = KMeans(n_clusters=f, random_state=2)
                kmeans = kmeans.fit(X_r_B)
                u = kmeans.inertia_
                inertia.append(u)
                print("The innertia for :", f, "Clusters is:", u)

            # Creating the scree plot for Intertia - elbow method
            fig, (ax1) = plt.subplots(1, figsize=(16,6))
            xx = np.arange(len(no_of_clusters))
            ax1.plot(xx, inertia)
            ax1.set_xticks(xx)
            ax1.set_xticklabels(no_of_clusters, rotation='vertical')
            plt.xlabel('n_components Value')
            plt.ylabel('Inertia Score')
            plt.title("Inertia Plot per k")
            with st.expander("re-iterating K means with with Data fitted on PCA 5 components"):
                st.pyplot()

            
            from sklearn import metrics
            from sklearn.metrics import davies_bouldin_score


            #rerunning with optimal pca and optimal K
            pca = PCA(n_components=5, random_state = 111)
            X_r_B = pca.fit(X_B).transform(X_B)

            # Running Kmeans with 6 Ks
            kmeans = KMeans(n_clusters=5, random_state=2)
            kmeans = kmeans.fit(X_r_B)

            clusters03 = kmeans.labels_

            with st.expander("model evaluation"):
                st.write('the silhouette score is')
                st.markdown(metrics.silhouette_score(X_r_B,clusters03))
                st.write('the davies bouldin indexscore')
                st.markdown(davies_bouldin_score(X_r_B,clusters03))
                st.write('the calinski harabasz index score')
                st.markdown(metrics.calinski_harabasz_score(X_r_B,clusters03))
                st.write("The Inertia is") 
                st.markdown(kmeans.inertia_)










            import plotly.express as px

            pca = PCA(n_components=3, random_state = 111)
            X_r_B3 = pca.fit(X_B).transform(X_B)
            X_r_B3df = pd.DataFrame(X_r_B3)

            # Running Kmeans with 5 Ks
            kmeans = KMeans(n_clusters=5, random_state=2)
            kmeans = kmeans.fit(X_r_B3df)

            clustersB3 = kmeans.labels_

            X_r_B3df['Clusters']=clustersB3

            total_var = pca.explained_variance_ratio_.sum() * 100

            fig = px.scatter_3d(
            X_r_B3, x=0, y=1, z=2, color=X_r_B3df['Clusters'],
            title=f'Total Explained Variance: {total_var:.2f}%',
            labels={'0': 'PC 1', '1': 'PC 2', '2': 'PC 3'}
            )
            with st.expander(" Visualization of PCA 3 Components with 90% variance"):
                st.plotly_chart(fig)


        if selected =='model 5':
            st.markdown("<h1 style='text-align: center; color: Red;'>K means without standarization</h1>", unsafe_allow_html=True)
            cols_use = data[['Calls_initiated', 'Average_waiting_duration',
       'totalfees', 'total_free_duration_used', 'usual_service_type',
       'normal_balance_after_call', 'total_deducted',
       'talk_time', 'calls_recieved_by_number', 'billable_minutes',
       'usual_call_type', 'usual_charge_type', 'usual_terminationreason',
       'count_of_recharges', 'sub_class_service', 'sum_of_facevalue',
       'frequent_recharge_type', 'rege_card_serviceclass']]
            encoded_cols_use = pd.get_dummies(cols_use)
            X_train_2 = encoded_cols_use.values
            no_of_clusters = range(2,30)
            inertia = []


            for f in no_of_clusters:
                kmeans = KMeans(n_clusters=f, random_state=222)
                kmeans = kmeans.fit(X_train_2)
                u = kmeans.inertia_
                inertia.append(u)
                print("The innertia for :", f, "Clusters is:", u)

                # Creating the scree plot for Intertia - elbow method
            fig, (ax1) = plt.subplots(1, figsize=(16,6))
            xx = np.arange(len(no_of_clusters))
            ax1.plot(xx, inertia)
            ax1.set_xticks(xx)
            ax1.set_xticklabels(no_of_clusters, rotation='vertical')
            plt.xlabel('Number of clusters')
            plt.ylabel('Inertia Score')
            plt.title("Inertia Plot per k")
            with st.expander("k selection - elbow method"):
                st.pyplot()


            kmeans = KMeans(n_clusters=5, random_state=2)
            kmeans = kmeans.fit(X_train_2)




            # "predictions" for new data
            predictions = kmeans.predict(X_train_2)

            # calculating the Counts of the cluster
            unique, counts = np.unique(predictions, return_counts=True)
            counts = counts.reshape(1,5)

            # Creating a datagrame
            countscldf = pd.DataFrame(counts, columns = ["Cluster 0","Cluster 1","Cluster 2", "Cluster 3","Cluster 4"])

            # display
            with st.expander("resulting clusters"):
                st.dataframe(countscldf)

            from sklearn.decomposition import PCA
            from sklearn.discriminant_analysis import LinearDiscriminantAnalysis


            X_2 = X_train_2
            y_num = predictions


            target_names = ["Cluster 0","Cluster 1","Cluster 2", "Cluster 3","Cluster 4"]

            pca = PCA(n_components=2, random_state = 111)
            X_r_2 = pca.fit(X_2).transform(X_2)


            print('Explained variance ratio (first two components): %s' % str(pca.explained_variance_ratio_))


            plt.figure()
            plt.figure(figsize=(12,8))
            colors = ['navy', 'turquoise', 'darkorange', 'red', 'black']
            lw = 2


            for color, i, target_name in zip(colors, [0, 1, 2, 3, 4], target_names):
                plt.scatter(X_r_2[y_num == i, 0], X_r_2[y_num == i, 1], color=color, alpha=.8, lw=lw,label=target_name)


            plt.legend(loc='best', shadow=False, scatterpoints=1)
            plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.6)   
            plt.title('PCA of 2 Components')
            with st.expander("PCA 2 components explaining 96% of variance"):
                st.pyplot()


            n_components = X_2.shape[1]

            # Running PCA with all components
            pca = PCA(n_components=n_components, random_state = 111)
            X_r_2 = pca.fit(X_2).transform(X_2)


            # Calculating the 95% Variance
            total_variance = sum(pca.explained_variance_)
            print("Total Variance in our dataset is: ", total_variance)
            var_95 = total_variance * 0.95
            print("The 95% variance we want to have is: ", var_95)
            print("")

            # Creating a df with the components and explained variance
            a = zip(range(0,n_components), pca.explained_variance_)
            a = pd.DataFrame(a, columns=["PCA Comp", "Explained Variance"])


            # Plotting the Data
            plt.figure(1, figsize=(14, 8))
            plt.plot(pca.explained_variance_ratio_, linewidth=2, c="r")
            plt.xlabel('n_components')
            plt.ylabel('explained_ratio_')

            # Plotting line with 95% e.v.
            plt.axvline(2,linestyle=':', label='n_components - 95% explained', c ="blue")
            plt.legend(prop=dict(size=12))

            # adding arrow
            plt.annotate('2 eigenvectors used to explain 95% variance', xy=(2, pca.explained_variance_ratio_[2]), 
             xytext=(2, pca.explained_variance_ratio_[2]),
            arrowprops=dict(facecolor='blue', shrink=0.05))

            with st.expander("Getting PCA component to hit 95% variance"):

                st.pyplot()

            pca = PCA(n_components=2, random_state = 111)
            X_r_2 = pca.fit(X_2).transform(X_2)

            inertia = []

            #running Kmeans

            for f in no_of_clusters:
                kmeans = KMeans(n_clusters=f, random_state=2)
                kmeans = kmeans.fit(X_r_2)
                u = kmeans.inertia_
                inertia.append(u)
                print("The innertia for :", f, "Clusters is:", u)

            # Creating the scree plot for Intertia - elbow method
            fig, (ax1) = plt.subplots(1, figsize=(16,6))
            xx = np.arange(len(no_of_clusters))
            ax1.plot(xx, inertia)
            ax1.set_xticks(xx)
            ax1.set_xticklabels(no_of_clusters, rotation='vertical')
            plt.xlabel('n_components Value')
            plt.ylabel('Inertia Score')
            plt.title("Inertia Plot per k")
            with st.expander("re-iterating K means with Data fitted on PCA 2 components"):
                st.pyplot()

            




       







           


            



           

            







           




        if selected=="model 6":
            st.markdown("<h1 style='text-align: center; color: Red;'>Gaussian Mixture Model</h1>", unsafe_allow_html=True)

            from sklearn.mixture import BayesianGaussianMixture
            from sklearn.preprocessing import PowerTransformer

            X_Gmm = data[['Calls_initiated', 'Average_waiting_duration', 'totalfees',
       'total_free_duration_used',
       'normal_balance_after_call', 'total_deducted',
       'talk_time', 'calls_recieved_by_number', 'billable_minutes',
       
       'count_of_recharges', 'sum_of_facevalue']]

            X_Gmm_transformed = PowerTransformer().fit_transform(X_Gmm)
            X_Gmm_transformed = pd.DataFrame(X_Gmm_transformed)

            gmm = BayesianGaussianMixture(n_components=6, max_iter=100, random_state=2)

            gmm_labels = gmm.fit_predict(X_Gmm_transformed)

            gmm_proba = gmm.predict_proba(X_Gmm_transformed)

            X_Gmm_transformed['clusters']= gmm_labels

            X_Gmm_transformed['probabilities']=np.max(gmm_proba, axis=1)

            x_Gmm_11 = X_Gmm_transformed.copy()

            x_Gmm_11.drop(columns=['clusters','probabilities'], axis=1, inplace=True)


            labelsgmm = gmm_labels
            from sklearn import metrics
            from sklearn.metrics import davies_bouldin_score

            with st.expander("model evaluation"):

                st.write('the silhouette score ')
                st.markdown(metrics.silhouette_score(x_Gmm_11,labelsgmm))
                st.write('the davies bouldin indexscore')
                st.markdown(davies_bouldin_score(x_Gmm_11,labelsgmm))
                st.write('the calinski harabasz index score ')
                st.markdown(metrics.calinski_harabasz_score(x_Gmm_11,labelsgmm))

            



        if selected =="model 7":
            
            st.markdown("<h1 style='text-align: center; color: Red;'>Agglomerative Clustering</h1>", unsafe_allow_html=True)



            with st.expander("Dendrogram"):
                html_string2="""<a href="https://im.ge/i/FJfjEW"><img src="https://i.im.ge/2022/08/10/FJfjEW.Screenshot-2022-08-10-200455.png" alt="Screenshot 2022-08-10 200455" border="0"></a>"""
                st.markdown(html_string2,unsafe_allow_html=True)

            from sklearn.cluster import AgglomerativeClustering 
            import scipy.cluster.hierarchy as sch

            cols_use = data[['Calls_initiated', 'Average_waiting_duration',
       'totalfees', 'total_free_duration_used', 'usual_service_type',
       'normal_balance_after_call', 'total_deducted',
       'talk_time', 'calls_recieved_by_number', 'billable_minutes',
       'usual_call_type', 'usual_charge_type', 'usual_terminationreason',
       'count_of_recharges', 'sub_class_service', 'sum_of_facevalue',
       'frequent_recharge_type', 'rege_card_serviceclass']]
            encoded_cols_use = pd.get_dummies(cols_use)

            from sklearn.preprocessing import MinMaxScaler
            enc_mm_cols_use = MinMaxScaler().fit_transform(encoded_cols_use.values)
            enc_mm_cols_use_df = pd.DataFrame(enc_mm_cols_use,index=encoded_cols_use.index, columns = encoded_cols_use.columns)





            X_Agg_mm = enc_mm_cols_use_df[['Calls_initiated', 'Average_waiting_duration', 'totalfees',
       'total_free_duration_used',
       'normal_balance_after_call', 'total_deducted',
       'talk_time', 'calls_recieved_by_number', 'billable_minutes',
       
       'count_of_recharges', 'sum_of_facevalue']]

            agg = AgglomerativeClustering(n_clusters = 5, affinity='euclidean', linkage='ward')
            agg.fit(X_Agg_mm)

            agglabels = agg.labels_
            from sklearn import metrics
            from sklearn.metrics import davies_bouldin_score

            with st.expander("model evaluation"):

                st.write('the silhouette score')
                st.markdown(metrics.silhouette_score(X_Agg_mm,agglabels))
                st.write('the davies bouldin indexscore')
                st.markdown(davies_bouldin_score(X_Agg_mm,agglabels))
                st.write('the calinski harabasz index score')
                st.markdown(metrics.calinski_harabasz_score(X_Agg_mm,agglabels))


    if menu_id=="Chosen Model":
        st.markdown("<h1 style='text-align: center; color: Red;'>Clustering using the best model</h1>", unsafe_allow_html=True)
        uploaded_data_2 = st.file_uploader('Upload dataset', type='csv')
        if uploaded_data_2:
            from sklearn.decomposition import PCA
            from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
            from sklearn.cluster import KMeans, k_means

            data=pd.read_csv(uploaded_data_2)

            cols_use = data[['Calls_initiated', 'Average_waiting_duration',
       'totalfees', 'total_free_duration_used', 'usual_service_type',
       'normal_balance_after_call', 'total_deducted',
       'talk_time', 'calls_recieved_by_number', 'billable_minutes',
       'usual_call_type', 'usual_charge_type', 'usual_terminationreason',
       'count_of_recharges', 'sub_class_service', 'sum_of_facevalue',
       'frequent_recharge_type', 'rege_card_serviceclass']]
            encoded_cols_use = pd.get_dummies(cols_use)

            from sklearn.preprocessing import MinMaxScaler
            enc_mm_cols_use = MinMaxScaler().fit_transform(encoded_cols_use.values)
            enc_mm_cols_use_df = pd.DataFrame(enc_mm_cols_use,index=encoded_cols_use.index, columns = encoded_cols_use.columns)
            
            num_mm =enc_mm_cols_use_df[['Calls_initiated', 'Average_waiting_duration', 'totalfees',
       'total_free_duration_used',
       'normal_balance_after_call', 'total_deducted',
       'talk_time', 'calls_recieved_by_number', 'billable_minutes',
       
       'count_of_recharges', 'sum_of_facevalue']]
            X_train_B = num_mm.values
            X_B = X_train_B

            pca = PCA(n_components=5, random_state = 111)
            X_r_B = pca.fit(X_B).transform(X_B)

            # Running Kmeans with 5 Ks
            kmeans = KMeans(n_clusters=5, random_state=2)
            kmeans = kmeans.fit(X_r_B)

            clustersB = kmeans.labels_

            dataB = data.copy()
            dataB['Clusters']=clustersB

            def convert_df(dataframe):
                return dataframe.to_csv(index= False)

            csv_data_clustered= convert_df(dataB)
            st.download_button(label="Export Clustered Data as CSV ", data=csv_data_clustered, file_name='newClustereddata.csv', mime='text/csv')

    if menu_id=="Classifier":
        uploaded_data_3 = st.sidebar.file_uploader('Upload dataset', type='csv')
        if uploaded_data_3:
            dfc=pd.read_csv(uploaded_data_3)
            X=dfc[['Calls_initiated','Average_waiting_duration','totalfees','total_free_duration_used','total_deducted','talk_time','calls_recieved_by_number','billable_minutes','count_of_recharges']]
            Y= dfc[['Clusters']]


            from sklearn.pipeline import Pipeline
            from sklearn.compose import ColumnTransformer
            from sklearn.preprocessing import MinMaxScaler
            from sklearn.preprocessing import OneHotEncoder
            from sklearn.ensemble import RandomForestClassifier

            num_vars = X.select_dtypes(include=['float', 'int']).columns.tolist()
            cat_vars = X.select_dtypes(include=['object']).columns.tolist()
            cat_encoder = OneHotEncoder(sparse=False, handle_unknown='ignore', drop = 'first')
            cat_pipeline = Pipeline([
            ('encoding', cat_encoder),
            ])
            num_pipeline = Pipeline([
            ('scaler', MinMaxScaler())])
            #Pipeline to apply on all columns
            full_pipeline = ColumnTransformer([
            ("num", num_pipeline, num_vars),
            ("cat", cat_pipeline, cat_vars),
            ])

            
            from xgboost import XGBClassifier

            #model = RandomForestClassifier(max_depth=30, max_features = 9, n_estimators = 150)
            model = XGBClassifier()
            pipeline = Pipeline(steps=[('i', full_pipeline), ('m', model)])

            from sklearn.model_selection import train_test_split
            X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=111)

            pipeline.fit(X_train,y_train)

            def user_report():
                cola,colb,colc,cold = st.columns([2,2,2,2])
                with cola:
                    Calls_initiated=st.number_input("calls initiated")
                    Average_waiting_duration=st.number_input("Average waiting duration")
                    totalfees=st.number_input("total fees")
                with colb:
                    total_free_duration_used=st.number_input("total free duration used")
                    total_deducted=st.number_input("total deducted")
                    talk_time=st.number_input("talk time")
                with colc:
                    calls_recieved_by_number=st.number_input("calls recieved")
                    billable_minutes=st.number_input("billables minutes")
                    count_of_recharges=st.number_input("count of recharges")

                user_report_data = {
                'Calls_initiated':Calls_initiated,
                'Average_waiting_duration':Average_waiting_duration,
                'totalfees':totalfees,
                'total_free_duration_used':total_free_duration_used,
                'total_deducted':total_deducted,
                'talk_time':talk_time,
                'calls_recieved_by_number':calls_recieved_by_number,
                'billable_minutes':billable_minutes,
                'count_of_recharges':count_of_recharges

                }   


                report_data =pd.DataFrame(user_report_data, index = [0])
                return report_data
			
            user_data = user_report()
            st.subheader('Prediction')
            st.dataframe(user_data)

            outcome = (pipeline.predict(user_data))
            st.subheader('Cluster Prediction')
            st.subheader(outcome)

            if outcome == 0:
                st.markdown(f'<h1 style="color:#6EFCFA;font-size:24px;">{"This Customer Belongs to the Diamond Category”"}</h1>', unsafe_allow_html=True)

            if outcome == 1:
                st.markdown(f'<h1 style="color:#943126;font-size:24px;">{"This Customer Belongs to the Bronze Category”"}</h1>', unsafe_allow_html=True)

            if outcome == 2:
                st.markdown(f'<h1 style="color:#F4D03F;font-size:24px;">{"This Customer Belongs to the Gold Category”"}</h1>', unsafe_allow_html=True)
     
            if outcome == 3:
                st.markdown(f'<h1 style="color:#D6DBDF ;font-size:24px;">{"This Customer Belongs to the Platinum Category”"}</h1>', unsafe_allow_html=True)
            
            if outcome == 4:
                st.markdown(f'<h1 style="color:#95A5A6 ;font-size:24px;">{"This Customer Belongs to the Silver Category”"}</h1>', unsafe_allow_html=True)
 
               


    if menu_id =="Social Network Analysis":
        st.markdown("<h1 style='text-align: center; color: Red;'>Social Network Analysis</h1>", unsafe_allow_html=True)
        
        import networkx as nx
        
        df=pd.read_csv('C:\\Users\\user\Downloads\\C__Users_user_Downloads_rawunique.csv')
        sn = df[['callingpartynumber','calledpartynumber']]
        sn_graph= nx.from_pandas_edgelist(sn, source="callingpartynumber",target="calledpartynumber")
        sn1 = nx.read_edgelist(sn)
        sn2= nx.read_edgelist(sn_graph)

        m1, m2 = st.columns(2)
        with m1:
                    
            theme_override = {'bgcolor': '#C8BFC4','title_color': '#0B0A0B', 'content_color': 'black', 'icon': 'fa fa-user', 'icon_color': 'Red'}
            hc.info_card(title = 'Number of Nodes', content = len(sn_graph.nodes()),
            theme_override=theme_override)
        with m2:
            theme_override = {'bgcolor': '#C8BFC4','title_color': '#0B0A0B', 'content_color': '000000', 'icon': 'fa fa-users', 'icon_color': 'Red'}
            hc.info_card(title = 'number of edges', content = len(sn_graph.edges()),
            theme_override=theme_override)
        
        
        from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
        import plotly.express as px
        import plotly.graph_objects as go
        nodesdegree = pd.DataFrame(list(sn_graph.degree),columns=['node','degree'])
        nodesdegree.sort_values(by='degree', ascending = False,inplace=True)
        df_nodesdegree=nodesdegree.groupby('degree')['node'].count().reset_index(name='counts')
        fig11 = px.scatter(df_nodesdegree, x='degree', y='counts')
        fig11 = go.Figure(fig11)
        with st.expander("distribution of degrees"):
            st.plotly_chart(fig11)
        
        top1 = nodesdegree.head(1)
        listtop1 = top1['node'].tolist()
        sntop1 = sn.loc[sn['callingpartynumber'].isin(listtop1) | sn['calledpartynumber'].isin(listtop1)]

        sntop1.reset_index(drop=True)

        st.markdown("<h1 style='text-align: center; color: red;'>Top 1 Most influential User </h1>", unsafe_allow_html=True)

        with st.expander("Connections of the Top 1 influential User"):
            
            st.markdown(f'<h1 style="color:#00FF04;font-size:24px;">{"User ID"}</h1>', unsafe_allow_html=True)
            
            st.write("c010b0eb24c4b6448bc5d59b08ab5246")

            st.markdown(f'<h1 style="color:#00FF04;font-size:24px;">{"Degree"}</h1>', unsafe_allow_html=True)

            st.write("30476")


            st.dataframe(sntop1)

            st.subheader("Input Number to Check if Connection is present")
            usercheck = st.text_input("input number")
            if sntop1['callingpartynumber'].str.contains(usercheck).any():
                st.markdown(f'<h1 style="color:#00FF04;font-size:24px;">{"They are connected”"}</h1>', unsafe_allow_html=True)

            else:
                st.markdown(f'<h1 style="color:#FF1000;font-size:24px;">{"No previous connection has been established"}</h1>', unsafe_allow_html=True)


        top2 = nodesdegree.iloc[[1]]
        listtop2 = top2['node'].tolist()
        sntop2 = sn.loc[sn['callingpartynumber'].isin(listtop2) | sn['calledpartynumber'].isin(listtop2)]

        st.markdown("<h1 style='text-align: center; color: red;'>Top 2nd Most influential User </h1>", unsafe_allow_html=True)

        with st.expander("Connections of Top 2nd Most influential User"):
            
            st.markdown(f'<h1 style="color:#00FF04;font-size:24px;">{"User ID"}</h1>', unsafe_allow_html=True)
            
            st.write("cb9b99a6b2a53574176faef9e6004ad3	")

            st.markdown(f'<h1 style="color:#00FF04;font-size:24px;">{"Degree"}</h1>', unsafe_allow_html=True)

            st.write("16899")


            



            st.dataframe(sntop2)

            usertocheck = st.text_input("input user number")
            if sntop2['callingpartynumber'].str.contains(usertocheck).any() or sntop2['calledpartynumber'].str.contains(usertocheck).any():
                st.markdown(f'<h1 style="color:#00FF04;font-size:24px;">{"They are connected”"}</h1>', unsafe_allow_html=True)

            else:
                st.markdown(f'<h1 style="color:#FF1000;font-size:24px;">{"No previous connection has been established"}</h1>', unsafe_allow_html=True)













            




if __name__ == '__main__':
	main()
