<template>
  <div>
    <v-app-bar light>
      <v-toolbar-title>Manage Users</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn color="primary" to="/main/admin/users/create">Create User</v-btn>
    </v-app-bar>
    <v-text-field
      v-model="search"
      append-icon="mdi-magnify"
      label="Search"
      single-line
      hide-details
      rounded
      outlined
      pa-4
      ma-4
    ></v-text-field>
    <v-data-table
      :headers="headers"
      :items="users"
      :search="search"
      dense
      sort-by="email"
    >
      <template v-slot:[`item.is_active`]="{ item }">
        <v-simple-checkbox
          v-model="item.is_active"
          disabled
        ></v-simple-checkbox>
      </template>
      <template v-slot:[`item.is_superuser`]="{ item }">
        <v-simple-checkbox
          v-model="item.is_superuser"
          disabled
        ></v-simple-checkbox>
      </template>
      <template v-slot:[`item.id`]="{ item }">
        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn
              text
              icon
              :to="{ name: 'main-admin-users-edit', params: { id: item.id } }"
            >
              <v-icon v-on="on">mdi-pencil</v-icon>
            </v-btn>
          </template>
          <span>Edit User</span>
        </v-tooltip>
        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn
              text
              icon
              @click="activateUser(item.id)"
              :disabled="item.is_active"
            >
              <v-icon v-on="on">mdi-account-convert</v-icon>
            </v-btn>
          </template>
          <span>Activate user and send "new account" email</span>
        </v-tooltip>
      </template>
    </v-data-table>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { readAdminUsers } from '@/store/admin/getters';
import { dispatchGetUsers } from '@/store/admin/actions';
import { dispatchActivateUser } from '@/store/main/actions';

@Component
export default class AdminUsers extends Vue {
  public search: string = '';

  public headers = [
    {
      text: 'Email',
      sortable: true,
      value: 'email',
      align: 'left'
    },
    {
      text: 'Full Name',
      sortable: true,
      value: 'full_name',
      align: 'left'
    },
    {
      text: 'Is Active',
      sortable: true,
      value: 'is_active',
      align: 'left'
    },
    {
      text: 'Is Superuser',
      sortable: true,
      value: 'is_superuser',
      align: 'left'
    },
    {
      text: 'Actions',
      value: 'id',
      sortable: false
    }
  ];

  get users() {
    return readAdminUsers(this.$store);
  }

  public async mounted() {
    await dispatchGetUsers(this.$store);
  }

  public async editUser(item) {
    this.$router.push('/users/edit/' + item.id).catch(err => {
      throw new Error(`Problem handling something: ${err}.`);
    });
  }

  public async activateUser(user_id: number) {
    await dispatchActivateUser(this.$store, user_id);
    await dispatchGetUsers(this.$store);
  }
}
</script>
