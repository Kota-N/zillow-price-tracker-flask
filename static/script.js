const addBtn = document.querySelector('.add-house-container button');
const deleteBtn = document.querySelector('.delete-house-container button');
const nameInput = document.getElementById('name-input');
const urlInput = document.getElementById('url-input');
const deleteInput = document.getElementById('delete-input');

addBtn.addEventListener('click', async () => {
  const reqData = {
    name: nameInput.value.trim(),
    url: urlInput.value.trim(),
  };

  if (!nameInput.value.trim() == '' || !urlInput.value.trim() == '') {
    if (
      confirm(`Insert a house?\n\nName: ${reqData.name}\nURL: '${reqData.url}'`)
    ) {
      try {
        const res = await fetch('/api/houses/add', {
          method: 'POST',
          headers: { 'Content-type': 'application/json' },
          body: JSON.stringify(reqData),
        });
        const data = await res.json();
        alert(`Inserted!\n\nItem: ${data.added_name[1]}`);
        console.log(data);
      } catch (error) {
        console.log(error);
        alert('Error!\n' + error);
      }

      nameInput.value = '';
      urlInput.value = '';
      location.reload();
    }
  } else alert('Cannot insert an empty value');
});

deleteBtn.addEventListener('click', async () => {
  const reqData = { name: deleteInput.value };

  if (confirm(`Delete a house?\n\nName: ${reqData.name}`)) {
    try {
      const res = await fetch('/api/houses/delete', {
        method: 'POST',
        headers: { 'Content-type': 'application/json' },
        body: JSON.stringify(reqData),
      });
      const data = await res.json();
      alert(`Deleted!\n\nItem: ${data.deleted_name}`);
      console.log(data);
    } catch (error) {
      console.log(error);
      alert('Error!\n' + error);
    }

    deleteInput.value = '';
    location.reload();
  }
});
