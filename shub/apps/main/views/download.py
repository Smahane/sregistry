'''

Copyright (c) 2017, Vanessa Sochat, All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

'''

from shub.apps.main.models import (
    Container, 
    Collection,
    Star
)

from django.shortcuts import (
    get_object_or_404, 
    render_to_response, 
    render, 
    redirect
)

from django.http import (
    JsonResponse,
    HttpResponse
)

from django.http.response import Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

import os
import re
import uuid

from .containers import get_container




#######################################################################################
# CONTAINER DOWNLOAD
#######################################################################################

def download_recipe(request,cid):
    '''manually add a tag to the collection
    '''
    container = get_container(cid)
    if "deffile" in container.metadata:
        recipe = container.metadata['deffile']
        filename = "Singularity.%s" %container.tag

        response = HttpResponse(recipe,
                                content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="%s"' %filename
        return response


def download_container(request,cid,secret):
    '''manually add a tag to the collection
    '''
    container = get_container(cid)

    # The secret must be up to date
    if container.secret != secret:
        return Http404

    filename = "%s.img" %container.get_uri().replace('/','-')
    response = HttpResponse(container.image.datafile.file,
                            content_type='application/img')
    response['Content-Disposition'] = 'attachment; filename="%s"' %filename
    return response