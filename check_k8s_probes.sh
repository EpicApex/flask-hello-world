#!/bin/bash

# Set deployment name and namespace
DEPLOYMENT_NAME="flask-hello-world-deployment"
NAMESPACE="default"

# Function to extract and check success count
check_probe_success() {
    local probe_type=$1
    local success_count=$(kubectl describe -n $NAMESPACE deployment.apps/$DEPLOYMENT_NAME \
                        | grep "$probe_type" \
                        | grep -o 'success=[0-9]*' \
                        | grep -o '[0-9]*')

    echo "Checking $probe_type probe:"
    # if greater than 0
    if [[ $success_count -gt 0 ]]; then
        echo "$probe_type probe successful more than 0 times."
    else
        echo "$probe_type probe has not been successful yet."
    fi
}

# Check Liveness and Readiness probes
check_probe_success "Liveness"
check_probe_success "Readiness"