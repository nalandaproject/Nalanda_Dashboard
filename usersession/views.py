import json, datetime, time, collections
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, render_to_response
from django.template import Context, loader
from account.usermastery import UserMasteryMeta
from .usersessiondata import userSessionPageData
from .constants import metrics
from django.contrib.auth.decorators import login_required
from account.views import construct_response
from account.models import UserInfoSchool, UserInfoClass, UserInfoStudent
from usersession.models import *
@login_required(login_url='/account/login/')
def get_page_meta_view(request):
    """
    This function implements the request receiving and response sending for get page meta details
    """   
    print ("Inside get_page_meta_view:", request.user)
    user = request.user
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    parent_level = data.get('parentLevel', -2)
    parent_id = int(data.get('parentId', '').strip())
    objUserMastery = UserMasteryMeta(user, parent_id, parent_level)
    objUserData = objUserMastery.getPageMeta(metrics)
    response_text = json.dumps(objUserData,ensure_ascii=False)
    return HttpResponse(response_text,content_type='application/json')

@login_required(login_url='/account/login/')
def get_page_data_view(request):
    """
    This function implements the request receiving and response sending for get page data

    """
    user = request.user
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    startTimestamp = data.get('startTimestamp', 0)
    endTimestamp = data.get('endTimestamp', 0)
    # topicID = data.get('contentId', '').strip()
    parentLevel = data.get('parentLevel', -1)
    parentID = int(data.get('parentId', '').strip())
    # channelID = data.get('channelId', '').strip()
    objUserSession = userSessionPageData(user, parentID, parentLevel, startTimestamp, endTimestamp)
    objUserSessionData = objUserSession.getPageData()
    response_object = construct_response(0, "", "", objUserSessionData)
    response_text = json.dumps(response_object,ensure_ascii=False)
    return HttpResponse(response_text, content_type='application/json')

@login_required(login_url='/account/login/')
def get_trend_data_view(request):
    """
    This function is used to show the mastery data in a graphical format
    """
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        params = json.loads(body_unicode)
        start_timestamp = params.get('startTimestamp','')
        start = datetime.datetime.fromtimestamp(start_timestamp)
        end_timestamp = params.get('endTimestamp', '')
        end = datetime.datetime.fromtimestamp(end_timestamp)
        level =params.get('level')
        item_id = params.get('itemId')
        
        data = None
        content = None
        # if topic_id == "-1":
        #     content = Content.objects.filter(topic_id='').first()
        # else:
        #     content = Content.objects.filter(topic_id=topic_id,channel_id=channel_id).first()
        # total_questions = content.total_questions
        # sub_topics_total = content.sub_topics_total
        total_students = 1.0
        if level == -1 or level == 0:
            pass
        elif level == 1:
            school = UserInfoSchool.objects.filter(school_id=item_id).first()
            total_students = school.total_students
            data = School.objects.filter(school_id=item_id,date__gte=start,date__lte=end).order_by('date')
            # else:
            #     data = School.objects.filter(school_id=item_id,date__gte=start,date__lte=end).order_by('date')
                # print(data)
        elif level == 2:
            classroom = UserInfoClass.objects.filter(class_id=item_id).first()
            total_students = classroom.total_students
            # if topic_id == "-1":
            #     data = Class.objects.filter(class_id=item_id,date__gte=start,date__lte=end).order_by('date')
            # else:
            data = Class.objects.filter(class_id=item_id,date__gte=start,date__lte=end).order_by('date')
        elif level == 3:
            # if topic_id == "-1":
            #     data = Student.objects.filter(student_id=item_id,date__gte=start,date__lte=end).order_by('date')
            # else:
            data = Student.objects.filter(student_id=item_id,date__gte=start,date__lte=end).order_by('date')
        res = {}
        series = []
        series.append({'name':'# Total Active Usage','isPercentage':False})
        points = []
        total_usersession_usage = 0
        # print ("data:", data)
        for ele in data:
            temp = []
            # print("ele.total_usage:", ele.total_usage)
            total_usersession_usage += ele.total_usage
            temp.append(time.mktime(ele.date.timetuple()))
            # temp.append(mastered_topics)
            # print("total_usersession_usage:", total_usersession_usage)
            k = total_usersession_usage/(total_students)
            # print ("k:", k)
            m, s = divmod(k, 60)
            temp.append(m)
            
            points.append(temp)
        # print ("points:", points)
        res['series'] = series
        res['points'] = points
        #data_str = serializers.serialize('json', data)
        response = construct_response(0,'','',res)
        response_text = json.dumps(response,ensure_ascii=False)
        return HttpResponse(response_text,content_type='application/json')
    else:
        response = construct_response(1111,'wrong request','wrong request','')
        response_text = json.dumps(response,ensure_ascii=False)
        return HttpResponse(response_text,content_type='application/json')