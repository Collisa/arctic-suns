
        let selectedRowId;

        function showModal(rowId){
            const modal = document.querySelector('#modal');
            selectedRowId = rowId;
            modal.classList.remove('hidden');
        }

        function deleteRow(){
            fetch(deleteURL, {
                method: 'POST',
                headers: { 'Content-type': 'application/x-www-form-urlencoded' },
                body: `id=${selectedRowId}`
            });

            const row = document.querySelector(`[data-id="${selectedRowId}"]`);
            row.remove();

            hideModal();
        }

        function hideModal(){
            const modal = document.querySelector('#modal');
            modal.classList.add('hidden');
        }