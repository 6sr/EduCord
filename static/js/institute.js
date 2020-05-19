function addBranch(ele) {
    var branch_code = `
        <input type="text" class="form-control" name="branch" placeholder="Enter Branch">
        <div class="input-group-append">
            <button class="btn btn-danger" type="button" onclick="removeBranch(this)"><i class="fas fa-times"></i></button>
        </div>
    `;
    var ele_child = document.createElement('DIV');
    ele_child.classList.add('input-group')
    ele_child.classList.add('form-group')
    ele_child.innerHTML = branch_code;
    ele.parentElement.parentElement.appendChild(ele_child);
}

function removeBranch(ele) {
    ele.parentElement.parentElement.remove();
}
